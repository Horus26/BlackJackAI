from Carddeck import Carddeck
from Player import Player


class GamestateManager :
    def __init__(self, playerNamesList, numberOfCarddecks):
        self.playerList = []
        self.playableCarddeck = []
        self.currentPlayer = None

        for i in range(numberOfCarddecks):
            self.playableCarddeck.extend(Carddeck().deck)

        self.initPlayers(playerNamesList)

    def initPlayers(self, playerNamesList):
        for playerName in playerNamesList:
            self.addPlayer(playerName)
    
    def addPlayer(self, playerName):
        self.playerList.append(Player(playerName, 34))

    def removePlayer(self, player):
        if player in self.playerList:
            self.playerList.remove(player)

    def printPlayableCarddeck(self):
        for card in self.playableCarddeck:
            print(card)
        print("CARD COUNT: " + str(len(self.playableCarddeck)))


# TODO: GAMEFLOW
if __name__ == "__main__":
    gamestateManager = GamestateManager(["Baek Jiheon, Lee Nagyung"], 3)
    gamestateManager.printPlayableCarddeck()