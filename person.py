import sys

from functions import *
from tables import *
import random


class Person:
    def __init__(self, internet, name):
        self.proceed = True
        self.agreed_curve = None
        self.internet = internet
        self.name = name
        self.partner = None

        self.goes_first = False
        self.initiated = False

        self.G = None
        self.proposed_curve = None

        self.secret_parameter = random.randint(3, 15)

        self.find_kxG = False
        self.kxG = None
        self.partner_kxG = None
        self.sent_kxG = False

        self.find_nGxk = False
        self.nGxk = None

        if self.name == "BOB":
            self.partner = "ALICE"
        else:
            self.partner = "BOB"

    def run(self):
        if self.proceed:
            if self.goes_first:
                proposed_curve = random.choice(CURVES)
                self.internet.send_message(self.name, self.partner, "AW1", proposed_curve)
                self.goes_first = False

            if self.find_kxG:
                self.calculate_kxG()
                self.find_kxG = False

            if self.kxG is not None and not self.sent_kxG:
                self.internet.send_message(self.name, self.partner, "KW1", self.kxG)
                self.sent_kxG = True

            if self.find_nGxk:
                self.calculate_nGxk()

            self.listen()

    def listen(self):
        message = self.internet.receive_message(self.name)

        if message:
            self.return_protocol(message)

    def return_protocol(self, message):
        match message[2]:
            case "AW1":
                print(f"[{self.name}] Agreed to curve {message[3]}")
                self.agreed_curve = message[3]
                self.internet.send_message(self.name, self.partner, "AW2", message[3])
                self.find_kxG = True
            case "AW2":
                print(f"[{self.name}] You agree, curve set to {message[3]}")
                self.agreed_curve = message[3]
                self.find_kxG = True
                print("--------- Connect complete ---------")
            case "KW1":
                print(f"[{self.name}] {self.partner} sent me their kxG: {message[3]}")
                self.partner_kxG = message[3]
                self.find_nGxk = True
            case "NIL":
                print(f"[{self.name}] {self.partner} is done: {message[3]}")


    def calculate_kxG(self):
        if self.agreed_curve == "secp256k1":
            self.kxG = scalar_multiply(self.secret_parameter,(68, 74), 97)

    def calculate_nGxk(self):
        print(f"[{self.name}] My secret: {self.secret_parameter}")
        print(f"[{self.name}] Computing {self.secret_parameter} × {self.partner_kxG}")

        self.nGxk = scalar_multiply(self.secret_parameter, self.partner_kxG, 97)



        print(f"[{self.name}] nGxk = {self.nGxk}")
        self.internet.send_message(self.name, self.partner, "NIL", "terminating")
        self.proceed = False
        print(f"[EVE] saw {self.internet.eve}")

