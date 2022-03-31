from abc import ABC, abstractmethod


PLAYER_ACTIONS = {
    "Hit" : 0,
    "Stand": 1,
    "Double": 2,
    "Split": 3
}

class Player(ABC) :
    def __init__(self, playerName, startMoney):
        self.name = playerName
        self.money = startMoney
        self.currentBet = 0
        self.cards = []

    def addCard(self, card):
        self.cards.append(card)
    
    def clearCards(self, card):
        self.cards.clear()

    
    def getBet(self):
        bet = self.determineBet()
        while(bet is not None and bet > self.money): 
            bet = self.determineBet()
        
        if bet is not None:
            self.money -= bet
            
        self.currentBet = bet
        return bet

    @abstractmethod
    def determineBet(self):
        pass

    @abstractmethod
    def makeTurn(self):
        pass

    def getHandValue(self):
        return sum([card.value for card in self.cards])




