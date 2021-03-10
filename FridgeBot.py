import re
from chatterbot import ChatBot, comparisons, filters, response_selection
from chatterbot.comparisons import levenshtein_distance
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from refrigerator_world_training import conversations, FridgeBot


def order_api(chatbot_response):
    """Looks for a triggering response from the FridgeBot and handles it."""
    if chatbot_response.text == 'createorder':
        p = re.compile(r'(\d+)? ?(gallons?|pounds?)?( of )?.*(milk|bacon|eggs?)')
        user_input = input('FridgeBot: Sounds like you want to place an order. What would item you like to order? You can choose eggs, bacon, or milk.\n' \
                     'User: ').lower()
        match = p.match(user_input)
        while not match:
       # while 'egg' not in item and 'bacon' not in item and 'milk' not in item:
            print("FridgeBot: Sorry, I didn't understand that. Please try again.")
            user_input = input('FridgeBot: I can currently only order milk, bacon, or eggs. What would you like to order?\n' \
                               'User: ').lower()
            match = p.match(user_input)

        quantity = match.group(1)
        units = match.group(2)
        item = match.group(4)

        if not quantity:
            user_input = input(f'FridgeBot: How many {units if units else ""}{" of " if units else ""}{item} would you like?\n' \
                                'User: ')
            p = re.compile(r'(\d+) ?({}s?|{}s?)?'.format(item, units))
            while True:
                try:
                    quantity = int(p.match(user_input).groups()[1])
                    break
                except TypeError:
                    print('FridgeBot: Invalid input, please enter an integer number.')
                    user_input = input(f'FridgeBot: How many {units if units else ""}{" of " if units else ""}{item} would you like?\n' \
                                        'User: ')
        else:
            quantity = int(quantity)        

        delivery = input('FridgeBot: When would you like the order delivered? You can choose morning, afternoon, or evening.\n' \
                         'User: ').lower()
        while delivery not in ('morning', 'afternoon', 'evening'):
            print('FridgeBot: Sorry, I can only accept "morning", "afternoon", and "evening" as delivery times. Please try again.')
            delivery = input('FridgeBot: When would you like the order delivered? You can choose morning, afternoon, or evening.\n' \
                             'User: ').lower()
        fridge.createOrder(item, units, quantity, delivery)

        reply = Statement(f'Great! Your order of {quantity} {units if units else ""}{" of " if units else ""}{item} will be delivered in the {delivery}.')

    elif chatbot_response.text == 'modifyorder':
        order = fridge.order
        if not order:
            reply = Statement('You have no pending order.')
        else:
            delivery = input(f'FridgeBot: Okay, I see your order for {order.item} coming in the {order.delivery_time}.\n' \
                            'FridgeBot: When would you like the order to be delivered? You can choose morning, afternoon, or evening.\n' \
                            'User: ').lower()
            order.delivery_time = delivery
            if 'milk' in order.item:
                item = 'gallon(s) of milk'
            elif 'bacon' in order.item:
                item = 'pound(s) of bacon'
            else:
                item = 'egg(s)'
            reply = Statement(f'All set! Your order of {order.quantity} {item} will now be delivered in the {delivery}.')

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
            reply = Statement(f'Your order of {order.quantity} {item} is scheduled to be delivered in the {order.delivery_time}.')

    # Future Capability  
    # elif chatbot_response.text == 'deleteorder':
    #     order = fridge.order
    #     if not order:
    #         reply = Statement('You have no pending order.')
    #     else:
    #         item = order.item
    #         fridge.order = None
    #         reply = Statement(f"I've cancelled your order for {item}.")
    
    elif chatbot_response.text == 'updatefridge':
        order = fridge.order
        item = order.item
        if 'milk' in item:
            fridge.milk += order.quantity
            print(f'FridgeBot: Great! Your order of {order.quantity} gallon(s) of milk was been added to the fridge.')
            reply = Statement(f'FridgeBot: You now have {fridge.milk} gallon(s) of milk in the fridge.')
        elif 'bacon' in item:
            fridge.bacon += order.quantity
            print(f'FridgeBot: Great! Your order of {order.quantity} pound(s) of bacon was been added to the fridge.')
            reply = Statement(f'FridgeBot: You now have {fridge.bacon} pound(s) of bacon in the fridge.')
        else:
            fridge.eggs += order.quantity
            print(f'FridgeBot: Great! Your order of {order.quantity} egg(s) was been added to the fridge.')
            reply = Statement(f'FridgeBot: You now have {fridge.eggs} egg(s) in the fridge.')
        
        fridge.order = None

    elif 'fridgecontents' in chatbot_response.text:
        if chatbot_response.text == 'fridgecontents':
            print("FridgeBot: Here's what's in the fridge:")
            print(f'\t{fridge.milk} gallon(s) of milk')
            print(f'\t{fridge.eggs} egg(s)')
            print(f'\t{fridge.bacon} pound(s) of bacon')
        elif 'milk' in chatbot_response.text:
            if fridge.milk == 0:
                print('FridgeBot: Uh oh, looks like you are out of milk!')
            else:
                print(f"FridgeBot: There are {fridge.milk} gallon(s) of milk in the fridge.")
        elif 'bacon' in chatbot_response.text:
            if fridge.bacon == 0:
                print('FridgeBot: Uh oh, looks like you are out of bacon!')
            else:
                print(f"FridgeBot: There are {fridge.bacon} pound(s) of bacon in the fridge.")
        elif 'eggs' in chatbot_response.text:
            if fridge.eggs == 0:
                print('FridgeBot: Uh oh, looks like you are out of eggs!')
            else:
                print(f"FridgeBot: There are {fridge.eggs} eggs in the fridge.")
        reply = Statement('What else can I help you with?')

    else:
        reply = chatbot_response

    if not reply.confidence:
        reply.confidence = 1.0
    
    return reply


fridge = FridgeBot(
    'FridgeBot',
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "maximum_similarity_threshold": 0.7
        },        
        'FridgeLogic.PreviousInputLogic'
    ],
    filters=[filters.get_recent_repeated_responses]
)       

# Give the bot some rudimentary conversation skills 
trainer = ChatterBotCorpusTrainer(fridge, show_training_progress=False)
#trainer.train('chatterbot.corpus.english.conversations')  # Do not use. Avoid unwanted/incorrect replies.
trainer.train('chatterbot.corpus.english.greetings')

# Train the bot on our set of fridge conversations
trainer = ListTrainer(fridge, show_training_progress=False)
for conversation in conversations:
    trainer.train(conversation)

# Set initial conditions
print("FridgeBot: Welcome to FridgeBot! Here's what's in the fridge:")
print('\t', fridge.milk, 'gallon(s) of milk')
print('\t', fridge.eggs, 'egg(s)')
print('\t', fridge.bacon, 'pound(s) of bacon')

# Run the bot (don't forget to cross your fingers)
print('FridgeBot: How may I be of assistance?')
user_input = input('User: ')
while user_input and user_input.lower() != 'exit':  # if user enters blank response or exit, chatbot exits.
    response = fridge.get_response(user_input)
    response = order_api(response)
    #print(f'{response} - confidence: {response.confidence}')  # debug
    if response.confidence >= 0.7:
        print(f'FridgeBot: {response}')
    else:
        print("FridgeBot: I'm sorry, I'm not quite sure how to respond to that. What else can I help you with?")
    user_input = input('User: ')
else:
    print('FridgeBot: Thank you for using FridgeBot. Enjoy your breakfast!')