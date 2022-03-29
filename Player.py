PLAYER_ACTIONS = {
    "Hit" : 0,
    "Stand": 1
}

class Player :
    def __init__(self, playerName, startMoney):
        self.name = playerName
        self.money = startMoney
        self.cards = []

    def addCard(self, card):
        self.cards.append(card)
    
    def clearCards(self, card):
        self.cards.clear()

    def makeTurn(self):
        # TODO: DECISION PROCESS
        return PLAYER_ACTIONS["Hit"]


