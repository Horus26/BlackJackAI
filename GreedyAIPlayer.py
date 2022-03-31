from Player import Player
from Constants import PLAYER_ACTIONS

class GreedyAIPlayer(Player) :
    def __init__(self, player_name, start_money):
        super(). __init__(player_name, start_money)

    def make_turn(self):
        print("GreedyAIPlayer Hit")
        return PLAYER_ACTIONS["Hit"]

    def determine_bet(self):
        print("GreedyAIPlayer {} determining bet".format(self.name))
        return 1
