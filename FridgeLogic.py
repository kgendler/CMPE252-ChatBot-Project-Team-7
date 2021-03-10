from chatterbot import filters
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
            self.previous_input = statement  # Do not run the first time
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        """Doing a really poor job of memory management here but I don't think it's critical for the current scope"""

        if 'order' in input_statement.text.lower():
            output = Statement ('')
            output.confidence = 0
            return output

        # These are classes so need to instantiate them before using their compare method
        LevDist = LevenshteinDistance()
        # SynDist = SynsetDistance()

        # These will store max values found so far as we iterate through our trained conversations
        LevDist_max = 0
        # SynDist_max = 0

        store_i = 0
        store_j = 0
        # Iterate through the conversations and entries in each, tracking the best match
        for i, conversation in enumerate(conversations):
            for j, entry in enumerate(conversation):
                if (j % 2) == 1:  # only analyze human inputs
                    continue

                if (j + 3) >= len(conversation):  # make sure enough entries remain in conversation for the logic below
                    continue

                statement = Statement(entry)  # must be Statement object for comparisons, not string

                LD = LevDist.compare(self.previous_input, statement)
                if LD > LevDist_max:
                    store_i = i
                    store_j = j
                    LevDist_max = LD
                    LD_statement = Statement(conversation[j+3])

                # SD = SynDist.compare(self.previous_input, statement)
                # if SD > SynDist_max:
                #     if SynDist.compare(Statement(conversation[i+2]), input_statement) > 0.9:
                #         SD += (1 - SD)/2  # give boost over competition if current statment is a good match in the right position in the same conversation
                #     SynDist_max = SD
                #     SD_statement = Statement(conversation[i+3])


        if LevDist.compare(Statement(conversations[store_i][store_j+2]), input_statement) > 0.9:
            LD = 10  # if current statment is a good match in the right position in the same conversation, it's probably right.

        # Having calculated the maximum confidences for each method, determine the winner and output that Statement object
        # Note that output here doesn't mean it'll be the final chosen output of the bot. Bot will compare confidence from
        # this and any other logic adapters and choose the output with the highest confidence.
        # if LevDist_max > SynDist_max:
        output = LD_statement
        output.confidence = LevDist_max

        # elif SynDist_max > LevDist_max:
        #     output = SD_statement
        #     output.confidence = SynDist_max

        # else:
        #     output = Statement('Not quite sure how to respond to that...')
        #     output.confidence = 0.1
        
        # print(f'LevDist: {LevDist_max}, {LD_statement}')
        # print(f'SynDist: {SynDist_max}, {SD_statement}')
        # print('PreviousLogicAdapter returning {} with confidence {}'.format(output.text, output.confidence))
        self.previous_input = input_statement
        return output


class OrderLogic(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        """Figure out if the statement from the user contains the word "order".
        
        There's gotta be a better way to decide whether or not to run this."""
        if 'order' in statement.text.lower():
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        """Determine how to respond."""
        search_results = self.search_algorithm.search(input_statement)

        # Search for the closest match to the input statement
        confidence = 0
        closest_match = search_results[0]
        for result in search_results:
            if result.confidence > confidence:
                confidence = result.confidence
                closest_match = result

        # Get the best first response
        response_list = list(self.chatbot.storage.filter(search_in_response_to=closest_match.search_text))
        response = response_list[0]

        if response.text == 'createorder':
            item = input('Sounds like you want to place an order. What would you like to order?\n')
            quantity = input('What quanitity would you like to order?\n')
            delivery = input('What would you like the order delivered? You can choose morning, afternoon, or evening.\n')
            self.chatbot.createOrder(item.lower(), quantity, delivery)
            if 'milk' in item.lower():
                item = 'gallon(s) of milk'
            elif 'bacon' in item.lower():
                item = 'pound(s) of bacon'
            else:
                item = 'egg(s)'

            response = Statement('Great! Your order of {} {} will be delivered in the {}.'.format(quantity, item, delivery))

        elif response.text == 'modifyorder':
            order = self.chatbot.order
            delivery = input('Okay, I see your order for {} coming in the {}. When would you like the order to be delivered? You can choose morning, afternoon, or evening.\n'.format(order.item, order.delivery_time))
            order.delivery_time = delivery
            if 'milk' in order.item:
                item = 'gallon(s) of milk'
            elif 'bacon' in order.item:
                item = 'pound(s) of bacon'
            else:
                item = 'egg(s)'
            response = Statement('All set! Your order of {} {} will now be delivered in the {}.'.format(order.quantity, item, delivery))

        elif response.text == 'orderstatus':
            order = self.chatbot.order
            if not order:
                response = Statement('You have no pending order.')
            else:
                if 'milk' in order.item:
                    item = 'gallon(s) of milk'
                elif 'bacon' in order.item:
                    item = 'pound(s) of bacon'
                else:
                    item = 'egg(s)'
                response = Statement('Your order of {} {} is scheduled to be delivered in the {}.'.format(order.quantity, item, order.delivery_time))
            
        elif response.text == 'deleteorder':
            order = self.chatbot.order
            if not order:
                response = Statement('You have no pending order.')
            else:
                item = order.item
                self.chatbot.order = None
                response = Statement("I've cancelled your order for {}.".format(item))

        response.confidence = 1.2
        return response


class TestLogic(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        print(statement.conversation)
        recent_repeated_responses = filters.get_recent_repeated_responses(
            self.chatbot,
            statement.conversation
        )
        print(recent_repeated_responses)
        statements_in_db = list(self.chatbot.storage.filter())
        for statement_in_db in statements_in_db:
            print(statement_in_db.conversation)
        return False


if __name__ == '__main__':
    from chatterbot import ChatBot
    from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
    testbot = ChatBot('Test', logic_adapters=['FridgeLogic.TestLogic', 'chatterbot.logic.BestMatch'])
    #trainer = ChatterBotCorpusTrainer(testbot)
    #trainer.train('chatterbot.corpus.english.greetings')
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