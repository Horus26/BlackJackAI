from Carddeck import Carddeck
from GreedyAIPlayer import GreedyAIPlayer
from Player import PLAYER_ACTIONS
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

    def initRound(self):
        # get bets from every player
        for player in self.playerList:
            bet = player.getBet()
            if bet is None: 
                self.playerList.remove(player)

        # deal one card each to every player
        self.dealCardRound()

        # then one card to the dealer
        # TODO: Implement dealer correctly
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
        card = choice(self.playableCarddeck)
        self.playableCarddeck.remove(card)
        return card

    def playRound(self):
        playerRoundValues = []
        # ask each player for their turn
        for player in self.playerList:
            turnValue = self.playerTurn(player)
            playerRoundValues.append(turnValue)

        self.evaluateRound(playerRoundValues)



    def playerTurn(self, player):
            playerTurnAction = player.makeTurn()

            # get new hand value
            handValue = player.getHandValue()

            # evaluate turn
            if playerTurnAction == PLAYER_ACTIONS["Hit"]: self.hit(player)
            elif playerTurnAction == PLAYER_ACTIONS["Double"]: self.double(player)
            elif playerTurnAction == PLAYER_ACTIONS["Split"]: self.split(player)
            # else player action stand which results in no action
            else: return handValue

            # check if player has no options left
            if handValue >= 21 or player.money is 0: return handValue
            
            # recursion
            return self.playerTurn(player)

    def hit(self, player):
        card = self.getRandomCard()
        player.addCard(card)

    def double(self):
        # TODO:
        pass

    def split(self):
        # TODO:
        pass

    def evaluateRound(self, playerRoundValues):
        # TODO: evaluate winners
        for i, handValue in enumerate(playerRoundValues):
            print("PLAYER: {} has hand value: {}".format(self.playerList[i].name, handValue))
    




# TODO: GAMEFLOW
if __name__ == "__main__":
    gamestateManager = GamestateManager(["Baek Jiheon", "Lee Nagyung"], 3)
    gamestateManager.startGame()