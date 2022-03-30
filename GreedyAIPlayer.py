from Player import PLAYER_ACTIONS, Player

class GreedyAIPlayer(Player) :
    def __init__(self, playerName, startMoney):
        super(). __init__(playerName, startMoney)

    def makeTurn(self):
        print("GreedyAIPlayer Hit")
        return PLAYER_ACTIONS["Hit"]

    def determineBet(self):
        print("GreedyAIPlayer {} determining bet".format(self.name))
        return 1
