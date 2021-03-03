from chatterbot import ChatBot
from random import randrange

conversations = [[
    'Where is the milk?',
    'Regular or Non-Fat?',
    'Regular.',
    'It is in the refrigerator, on the left side.'
],
[
    'Where is the milk?',
    'Regular or Non-Fat?',
    'Non-Fat.',
    'I’m not sure.  Maybe there is some in the freezer.'
],
[
    'Where is the Regular milk?',
    'There should be some in the refrigerator.',
    'I am not finding any.',
    'Did you look on the right side?'
],
[
    'Where is the Non-Fat milk?',
    'I think we are out.  Should I order some?',
    'Yes, please.',
    'Ok.  I will ask them to deliver it today.'
],
[
    'Do we have any Non-Fat milk?',
    'We have powdered Non-Fat milk in the garage.',
    'Is there any in the refrigerator?',
    'No. Just in the garage.'  # This response was not given. "I am not finding any." was the bot's reply.
],
[
    'What do we have in the refrigerator to eat?',
    'Milk, eggs and bacon.',
    'What kind of milk',
    'Regular.'
],
[
    'Are we out of bacon?',
    'Did you look in the refrigerator?',
    'Yes, but I didn’t see any.',
    'Did you look behind the milk?'
],
[
    'Do we have any hard boiled eggs?',
    'Yes, in the refrigerator',
    'I don’t see them.',
    'Did you look behind the milk?'  # bot replied with "What kind of movies do you like?"
],
[
    'Do we have any uncooked eggs?',
    'What kind?',
    'Brown eggs.',
    'No.  We don’t have any brown eggs.',
    'Why not?',
    'You didn’t buy any.'  # bot replied with "Because I have never been inside the refrigerator when the door was closed."
],
[
    'Do we have any uncooked eggs?',
    'What kind?',
    'Any kind.',
    'Look behind the milk.',
    'Oh, there it is.  Thank you.',
    'What would you do without me?'
],
[
    'Who ate all of the eggs?',
    'We have eggs.',
    'Where?',
    'Did you look behind the milk?',
    'Oh, there it is.  Thank you.',
    'What would you do without me?'
],
[
    'Do we have any bacon left',
    'Did you look behind the milk?',
    'No.  I don’t need to look behind the milk.',
    'Please, look behind the milk.',
    'Oh, there it is.  Thank you.',
    'Try looking behind the milk before you ask me next time.'  # bot replied with "What would you do without me?"
],
[  # Karl: I think we should omit this conversation... Do we have milk, did you look being the milk... no milk.. kind of confusing. (But funny!)
    'Do we have any milk?',
    'Did you look behind the milk?',  # Bot replied with "Regular or Non-Fat?"
    'No.',
    'Please, look behind the milk.',
    'Ok. I am looking behind the milk but all I see are eggs and bacon.',
    'I guess we are out of milk, then.'
],
[
    'Where is the chocolate milk? ',
    'We don’t have chocolate milk, only regular or non-fat milk.',
    'Where is the regular milk?',
    'In the refrigerator, in front of the bacon.'  # bot replied with "There should be some in the refrigerator."
],
[
    'Do we have any frozen pizza?',
    'No.  You ate it all.',
    'Are you sure?',
    'Yes, I am sure.',  # bot replied with "Just because I'm software does not mean that I cannot experience existence."
    'Are you really sure?',
    'Yes, I am really sure.  Go do your homework.'
],
[
    'Where should I put the milk?',
    'In the refrigerator.',
    'Where in the refrigerator?',
    'Put the milk in front of the eggs, or in front of the bacon.',  # bot replied with "I am not finding any."
    'Ok, is there anything else in the refrigerator?',
    'No, just eggs, milk and bacon.'
],
[
    'Do we have any deviled eggs?',
    'No, we only have raw or hard-boiled eggs.',
    'Why don’t we have any deviled eggs?',
    'I don’t know.  You can make some yourself if you want them.',
    'I am too lazy to cook right now.',
    'Then no devilled-eggs for you.'
],
[
    'I am hungry',
    'Why don’t you get some food out of the refrigerator?',
    'I only see milk in the refrigerator.',
    'Are you sure?',
    'Yes.  I am sure.',
    'Did you look behind the milk?'
],
[
    'Does the refrigerator light stay on after I close the door?',
    'I don’t know.',
    'Why not?',
    'Because I have never been inside the refrigerator when the door was closed.',
    'Why not?',
    'Because it is dangerous.'  # Bot replies with "Because I have never been inside the refigerator when the door was closed."
],
[
    'How many much do we have in the refrigerator?',
    'count',
],
[
    'What is the status of my order?',
    'order status'
],
[
    "I'd like to reschedule my order.",
    'reschedule',
]
]

class Order(object):
    def __init__(self, item, quantity, address, delivery_time):
        self.item = item
        self.quantity = quantity
        self.address = address
        self.delivery_time = delivery_time

class FridgeBot(ChatBot):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.order = None
        self.milk = randrange(1,2)
        self.eggs = randrange(1,24)
        self.bacon = randrange(1,5)

        self.inputs = []
        self.best_matches = []
        self.outputs = []

    def consume(self, item, amount):
        """Remove an amount of milk, eggs, or bacon from the fridge."""
        if item == 'milk':
            self.milk -= amount
            if self.milk < 0:
                self.milk == 0
        elif item == 'eggs':
            self.eggs -= amount
            if self.eggs < 0:
                self.eggs == 0
        elif item == 'bacon':
            self.bacon -= amount
            if self.bacon < 0:
                self.bacon == 0
    
    def store(self, item, amount):
        """Add an amount of milk, eggs, or bacon to the fridge."""
        if item == 'milk':
            self.milk += amount
        elif item == 'eggs':
            self.eggs += amount
        elif item == 'bacon':
            self.bacon += amount
    
    def createOrder(self, item, quantity, address, delivery_time):
        """Add an order for an item.

        In the future, can append new order to a list, add other functionality to handle multiple orders."""
        self.order = Order(item, quantity, address, deliver_time)

    def logInput(self, user_input):
        """Add to the list of the last up to 10 user inputs"""
        self.inputs.append(user_input)
        if len(self.inputs) > 10:
            self.inputs = self.inputs[:10]
    
    def logBestMatch(self, best_match):
        """Add to the list of the last up to 10 best matches to the user inputs"""
        self.best_matches.append(best_match)
        if len(self.best_matches) > 10:
            self.best_matches = self.best_matches[:10]

    def logOutput(self, output):
        """Add to the list of the last up to 10 bot outputs"""
        self.outputs.append(output)
        if len(self.outputs) > 10:
            self.outputs = self.outputs[:10]
