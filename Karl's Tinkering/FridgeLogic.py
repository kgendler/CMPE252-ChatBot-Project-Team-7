from chatterbot.comparisons import LevenshteinDistance, JaccardSimilarity, SynsetDistance
from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter, BestMatch
from refrigerator_world_training import conversations


class PreviousInputLogic(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.previous_input = Statement('')

    def can_process(self, statement):
        if self.previous_input.text != '':
            return True
        else:
            self.previous_input = statement  # Current Statement object
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        """Doing a really poor job of memory management here but I don't think it's critical for the current scope"""

        # These are classes so need to instantiate them before using their compare method
        LevDist = LevenshteinDistance()
        JacSim = JaccardSimilarity()
        SynDist = SynsetDistance()

        # These will store max values found so far as we iterate through our trained conversations
        # This definitely feels like cheating.
        LevDist_max = 0
        JacSim_max = 0
        SynDist_max = 0

        # Iterate through the conversations and entries in each, tracking the best match
        for conversation in conversations:
            for i, entry in enumerate(conversation):
                if (i % 2) == 1:  # only analyze human inputs
                    continue

                if (i + 3) >= len(conversation):  # make sure enough entries remain in conversation for the logic below
                    continue

                statement = Statement(entry)  # must be Statement object for comparisons, not string

                LD = LevDist.compare(self.previous_input, statement)
                if LD > LevDist_max:
                    if LevDist.compare(Statement(conversation[i+2]), input_statement) > 0.9:
                        LD += (1 - LD)/2  # give 50% boost over competition if current statment is a good match in the right position in the same conversation
                    LevDist_max = LD
                    LD_statement = Statement(conversation[i+3])

                #JS = JacSim.compare(self.previous_input, statement)
                #if JS > JacSim_max:
                    #if JacSim.compare(Statement(conversation[i+2]), input_statement) > 0.9:
                        #JS += (1 - JS)/2  # give 50% boost over competition if current statment is a good match in the right position in the same conversation
                    #JacSim_max = JS
                    #JS_statement = Statement(conversation[i+3])

                SD = SynDist.compare(self.previous_input, statement)
                if SD > SynDist_max:
                    if SynDist.compare(Statement(conversation[i+2]), input_statement) > 0.9:
                        SD += (1 - SD)/2  # give 50% boost over competition if current statment is a good match in the right position in the same conversation
                    SynDist_max = SD
                    SD_statement = Statement(conversation[i+3])

        # Having calculated the maximum confidences for each method, determine the winner and output that Statement object
        # Note that output here doesn't mean it'll be the final chosen output of the bot. Bot will compare confidence from
        # this and any other logic adapters and choose the output with the highest confidence.
        if LevDist_max > JacSim_max and LevDist_max > SynDist_max:
            output = LD_statement
            output.confidence = LevDist_max

        elif JacSim_max > LevDist_max and JacSim_max > SynDist_max:
            output = JS_statement
            output.confidence = JacSim_max

        elif SynDist_max > LevDist_max and SynDist_max > JacSim_max:
            output = SD_statement
            output.confidence = SynDist_max

        else:
            output = Statement('Not quite sure how to respond to that...')
            output.confidence = 0.1
        
        return output
        

if __name__ == '__main__':
    from chatterbot import ChatBot
    from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
    testbot = ChatBot('Test', logic_adapters=['FridgeLogic.PreviousInputLogic', 'chatterbot.logic.BestMatch'])
    trainer = ChatterBotCorpusTrainer(testbot)
    trainer.train('chatterbot.corpus.english.greetings')
    trainer = ListTrainer(testbot)
    for conversation in conversations:
        trainer.train(conversation)
    print('Welcome to FridgeBot! How may I be of assistance?')
    user_input = input()
    while user_input:  # if user enters blank response, chatbot exits.
        response = testbot.get_response(user_input)
        print(response)
        user_input = input()
    else:
        print('Now exiting FridgeBot. Enjoy your breakfast!')