from chatterbot import ChatBot
from random import randrange

conversations = [[
    'Where is the milk?',
    'There should be some in the refrigerator on the left side.',
    'I am not finding any.',
    'fridgecontents-milk'
],
[
    'What do we have in the refrigerator?',
    'fridgecontents'
],
[    
    'What is in the fridge?',
    'fridgecontents'
],
[
    'Are we out of bacon?',
    'fridgecontents-bacon'
],
[
    'Do we have any bacon left',
    'fridgecontents-bacon'
],
[
    'Do we have any eggs?',
    'fridgecontents-eggs'
],
[
    'Who ate all of the eggs?',
    "Well it certainly wasn't me!"
],
[ 
    'Do we have any milk?',
    'fridgecontents-milk'
],
[
    'Where is the chocolate milk? ',
    'We don’t have chocolate milk, only regular milk.',
    'Where is the regular milk?',
    'There should be some in the refrigerator on the left side.'
],
[
    'Do we have any frozen pizza?',
    'fridgecontents'
],
[
    'Are you sure?',
    'Yes, I am sure.  Go do your homework ya lazy bum.'
],
[
    'Where should I put the milk?',
    'In the refrigerator, on the left side.',
],
[
    'Do we have any deviled eggs?',
    'No, we only have raw eggs.',
    'Why don’t we have any deviled eggs?',
    'I don’t know.  You can make some yourself if you want them.',
    'I am too lazy to cook right now.',
    'Then no deviled-eggs for you.'
],
[
    'I am hungry',
    'Why don’t you get some food out of the refrigerator?'
],
[
    'Does the refrigerator light stay on after I close the door?',
    'I don’t know, I have never been inside the refrigerator when the door was closed.',
    'Why not?',
    'Because it is dangerous. Let us never speak of this again.'
],
[
    'What is the status of my order',
    'orderstatus'
],
[
    'Reschedule my order',
    'modifyorder',
],
[
    'Schedule an order',
    'createorder'
],
[
    "I'd like to place an order",
    'createorder'
],
[
    'Thank you',
    'You are welcome!'
],
[
    'Where is my order?',
    'orderstatus'
],
[
    'My order has arrived!',
    'updatefridge'
],
]

class Order(object):
    def __init__(self, item, units, quantity, delivery_time):
        self.item = item
        self.units = units
        self.quantity = quantity
        self.delivery_time = delivery_time


class FridgeBot(ChatBot):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.order = None
        self.milk = randrange(1,3)
        self.eggs = randrange(1,25)
        self.bacon = randrange(1,5)

        # self.inputs = []
        # self.best_matches = []
        # self.outputs = []

    def createOrder(self, item, units, quantity, delivery_time):
        """Add an order for an item.

        In the future, can append new order to a list, add other functionality to handle multiple orders."""
        self.order = Order(item, units, quantity, delivery_time)

    # Here lies unimplemented functionality. RIP.

#                  ______
#            _____/      \\_____
#           |  _     ___   _   ||
#           | | \     |   | \  ||
#           | |  |    |   |  | ||
#           | |_/     |   |_/  ||
#           | | \     |   |    ||
#           | |  \    |   |    ||
#           | |   \. _|_. | .  ||
#           |                  ||
#           |    functions     ||
#           |                  ||
#   *       | *   **    * **   |**      **
#    \))..),,/.,(//,,..,,\||(,,.,\\,.((//

    # def consume(self, item, amount):
    #     """Remove an amount of milk, eggs, or bacon from the fridge."""
    #     if item == 'milk':
    #         self.milk -= amount
    #         if self.milk < 0:
    #             self.milk == 0
    #     elif item == 'eggs':
    #         self.eggs -= amount
    #         if self.eggs < 0:
    #             self.eggs == 0
    #     elif item == 'bacon':
    #         self.bacon -= amount
    #         if self.bacon < 0:
    #             self.bacon == 0
    
    # def store(self, item, amount):
    #     """Add an amount of milk, eggs, or bacon to the fridge."""
    #     if item == 'milk':
    #         self.milk += amount
    #     elif item == 'eggs':
    #         self.eggs += amount
    #     elif item == 'bacon':
    #         self.bacon += amount

    # def logInput(self, user_input):
    #     """Add to the list of the last up to 10 user inputs"""
    #     self.inputs.append(user_input)
    #     if len(self.inputs) > 10:
    #         self.inputs = self.inputs[:10]
    
    # def logBestMatch(self, best_match):
    #     """Add to the list of the last up to 10 best matches to the user inputs"""
    #     self.best_matches.append(best_match)
    #     if len(self.best_matches) > 10:
    #         self.best_matches = self.best_matches[:10]

    # def logOutput(self, output):
    #     """Add to the list of the last up to 10 bot outputs"""
    #     self.outputs.append(output)
    #     if len(self.outputs) > 10:
    #         self.outputs = self.outputs[:10]
