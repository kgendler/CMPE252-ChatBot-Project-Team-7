from chatterbot import comparisons, response_selection
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

bot = ChatBot(
    'Norman',
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": comparisons.levenshtein_distance,
            "response_selection_method": response_selection.get_first_response
        }
    ]
)

trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.english')

while True:
    try:
        user_input = input()
        if user_input == 'exit':
            break
        bot_response = bot.get_response(user_input)
        print(bot_response)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break