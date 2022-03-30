from random import getrandbits
import secrets
from Carddeck import Carddeck
from GreedyAIPlayer import GreedyAIPlayer
from secrets import choice

class GamestateManager :
    def __init__(self, playerNamesList, numberOfCarddecks):
        self.playerList = []
        self.playableCarddeck = []
        self.currentPlayer = None

        for i in range(numberOfCarddecks):
            self.playableCarddeck.extend(Carddeck().deck)

        if len(playerNamesList) == 0: return

        self.initPlayers(playerNamesList)
        self.startGame()

    def initPlayers(self, playerNamesList):
        for playerName in playerNamesList:
            self.addPlayer(playerName)
    
    def addPlayer(self, playerName):
        self.playerList.append(GreedyAIPlayer(playerName, 34))

    def removePlayer(self, player):
        if player in self.playerList:
            self.playerList.remove(player)

    def printPlayableCarddeck(self):
        for card in self.playableCarddeck:
            print(card)
        print("CARD COUNT: " + str(len(self.playableCarddeck)))

    def startGame(self):
        self.initRound()
        self.playRound()
        self.evaluateRound()

    def initRound(self):
        # get bets from every player
        for player in self.playerList:
            bet = player.getBet()
            if bet is None: 
                self.playerList.remove(player)

        # deal one card each to every player
        self.dealCardRound()

        # then one card to the dealer
        dealerCard = self.getRandomCard()

        # then the second card to every player
        self.dealCardRound()

        # then a face down second card to the dealer
        secondDealerCard = self.getRandomCard()
        
    
    def dealCardRound(self):
        for player in self.playerList:
            # draw random card
            card = self.getRandomCard()
            # assign card to player
            player.addCard(card)

    def getRandomCard(self):
        card = secrets.choice(self.playableCarddeck)
        self.playableCarddeck.remove(card)
        return card

    def playRound(self):
        # ask each player for their turn
        pass

    def evaluateRound(self):
        # evaluate winners
        pass
    




# TODO: GAMEFLOW
if __name__ == "__main__":
    gamestateManager = GamestateManager(["Baek Jiheon", "Lee Nagyung"], 3)
    # gamestateManager.printPlayableCarddeck()