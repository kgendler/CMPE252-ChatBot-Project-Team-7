from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import comparisons, response_selection
from chatterbot.comparisons import levenshtein_distance
from refrigerator_world_training import conversations

chatbot = ChatBot(
    'FridgeBot',
    logic_adapters=[
        #'chatterbot.logic.MathematicalEvaluation',
        #'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
    ]
)
        #'chatterbot.comparisons.levenshtein_distance',
        #"statement_comparison_function": chatterbot.JaccardSimilarity,
        #"statement_comparison_function": chatterbot.comparisons.SynsetDistance,
        #'chatterbot.response_selection.get_first_response',
        #"response_selection_method": chatterbot.response_selection.get_most_frequent_response,
        
        
trainer = ChatterBotCorpusTrainer(chatbot)

# Karl: I think we should limit the training to only the subset of corpus information needed.
#       This way we can avoid any unintended responses from things that our bot doesn't need to know about.
#       i.e. history, trivia, emotion, etc.
# trainer.train('chatterbot.corpus.english.conversations')  # commenting this out too to try to avoid more unneeded replies
trainer.train('chatterbot.corpus.english.greetings')


trainer = ListTrainer(chatbot)
for conversation in conversations:
    trainer.train(conversation)


print('Welcome to FridgeBot! How may I be of assistance?')
user_input = input()
while user_input:  # if user enters blank response, chatbot exits.
    response = chatbot.get_response(user_input)
    print(response)
    user_input = input()
else:
    print('Now exiting FridgeBot. Enjoy your breakfast!')