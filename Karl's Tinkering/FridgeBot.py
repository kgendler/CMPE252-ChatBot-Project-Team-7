from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import comparisons, response_selection
from chatterbot.comparisons import levenshtein_distance
from refrigerator_world_training import conversations, FridgeBot

fridge = FridgeBot(
    'FridgeBot',
    logic_adapters=[
        'FridgeLogic.PreviousInputLogic',
        'FridgeLogic.OrderLogic',
        'chatterbot.logic.BestMatch'
    ]
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
    print(response)
    user_input = input()
else:
    print('Now exiting FridgeBot. Enjoy your breakfast!')