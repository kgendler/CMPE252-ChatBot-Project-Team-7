from chatterbot import ChatBot, comparisons, filters, response_selection
from chatterbot.comparisons import levenshtein_distance
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from refrigerator_world_training import conversations, FridgeBot

def order_handler(chatbot_response):
    """Looks for a triggering response from the FridgeBot and handle an order, if needed."""
    if chatbot_response.text == 'createorder':
        item = input('Sounds like you want to place an order. What would you like to order?\n')
        quantity = input('What quantity would you like to order?\n')
        delivery = input('What would you like the order delivered? You can choose morning, afternoon, or evening.\n')
        fridge.createOrder(item.lower(), quantity, delivery)
        if 'milk' in item.lower():
            item = 'gallon(s) of milk'
        elif 'bacon' in item.lower():
            item = 'pound(s) of bacon'
        else:
            item = 'egg(s)'

        reply = Statement('Great! Your order of {} {} will be delivered in the {}.'.format(quantity, item, delivery))

    elif chatbot_response.text == 'modifyorder':
        order = fridge.order
        delivery = input('Okay, I see your order for {} coming in the {}. When would you like the order to be delivered? You can choose morning, afternoon, or evening.\n'.format(order.item, order.delivery_time))
        order.delivery_time = delivery
        if 'milk' in order.item:
            item = 'gallon(s) of milk'
        elif 'bacon' in order.item:
            item = 'pound(s) of bacon'
        else:
            item = 'egg(s)'
        reply = Statement('All set! Your order of {} {} will now be delivered in the {}.'.format(order.quantity, item, delivery))

    elif chatbot_response.text == 'orderstatus':
        order = fridge.order
        if not order:
            reply = Statement('You have no pending order.')
        else:
            if 'milk' in order.item:
                item = 'gallon(s) of milk'
            elif 'bacon' in order.item:
                item = 'pound(s) of bacon'
            else:
                item = 'egg(s)'
            reply = Statement('Your order of {} {} is scheduled to be delivered in the {}.'.format(order.quantity, item, order.delivery_time))
        
    elif chatbot_response.text == 'deleteorder':
        order = fridge.order
        if not order:
            reply = Statement('You have no pending order.')
        else:
            item = order.item
            fridge.order = None
            reply = Statement("I've cancelled your order for {}.".format(item))
    
    else:
        reply = chatbot_response

    if not reply.confidence:
        reply.confidence = 0.999
    
    return reply


fridge = FridgeBot(
    'FridgeBot',
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        'FridgeLogic.PreviousInputLogic'
    ],
    filters=[filters.get_recent_repeated_responses]
)       

# Give the bot some rudimentary conversation skills 
trainer = ChatterBotCorpusTrainer(fridge)
# trainer.train('chatterbot.corpus.english.conversations')  # commenting this out to avoid unwanted/incorrect replies
trainer.train('chatterbot.corpus.english.greetings')

# Train the bot on our set of fridge conversations
trainer = ListTrainer(fridge)
for conversation in conversations:
    trainer.train(conversation)

# Set initial conditions
print("Welcome to FridgeBot! Here's what's in the fridge:")
print('\t', fridge.milk, 'gallon(s) of non-fat milk')
print('\t', fridge.eggs, 'egg(s)')
print('\t', fridge.bacon, 'pound(s) of bacon')

# Run the bot (don't forget to cross your fingers)
print('How may I be of assistance?')
user_input = input()
while user_input:  # if user enters blank response, chatbot exits.
    response = fridge.get_response(user_input)
    #print(f"response: {type(response)}")
    response = order_handler(response)
    if response.confidence >= 0.7:
        print(response)
    else:
        print('WHAT? WHAT DID YOU SAY?')
    user_input = input()
else:
    print('Now exiting FridgeBot. Enjoy your breakfast!')