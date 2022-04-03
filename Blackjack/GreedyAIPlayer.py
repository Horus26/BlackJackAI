from .Player import Player
from .Constants import PLAYER_ACTIONS

class GreedyAIPlayer(Player) :
    def __init__(self, player_name, start_money):
        super(). __init__(player_name, start_money)

    def make_turn(self):
        # print("{} Hit".format(self.name))
        return PLAYER_ACTIONS["Hit"]

    def determine_bet(self):
        bet = 1
        print("GreedyAIPlayer {} determining bet: {}".format(self.name, bet))
        return bet
