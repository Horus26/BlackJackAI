from .Player import Player
from .Constants import PLAYER_ACTIONS

class GUIPlayer(Player) :
    def __init__(self, player_name, start_money):
        super(). __init__(player_name, start_money)
        self.gui_player = True

    def make_turn(self):
        # print("{} Hit".format(self.name))
        return PLAYER_ACTIONS["Hit"]

    def determine_bet(self):
        pass
