import random

from internet import Internet
from person import Person

class Controller:
    def __init__(self):

        self.internet = Internet()
        self.bob = Person(self.internet, "BOB")
        self.alice = Person(self.internet, "ALICE")


        self.people = [self.bob, self.alice]

        person = random.choice(self.people)
        person.goes_first = True


    def run(self):
        for person in self.people:
            person.run()

