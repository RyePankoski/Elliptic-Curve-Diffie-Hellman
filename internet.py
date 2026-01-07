class Internet:
    def __init__(self):
        self.messages = []
        self.eve = []


    def receive_message(self, recipient):
        for message in self.messages:
            if message[1] == recipient:
                to_recipient = message
                self.messages.remove(message)
                return to_recipient
        return None

    def send_message(self, sender, recipient, protocol, message):
        print(f"[{sender}] Sends packet to {recipient}: {protocol} + {message}")
        self.messages.append([sender, recipient, protocol, message])
        self.eve.append([sender, recipient, protocol, message])



