from .Player import Player
from .Constants import PLAYER_ACTIONS

class SplitTempPlayer(Player) :
    def __init__(self, player, card):
        super(). __init__(player.name + "_split", 0)
        self.parent_player = player
        self.current_bet = player.current_bet
        self.cards.append(card)
        # ensure that no resplitting can happen
        self.split_this_round = True

    def make_turn(self):
        # print("{} Hit".format(self.name))
        # TODO: IMPLEMENT CORRECT TURN ACTION DETERMINATION
        return PLAYER_ACTIONS["Stand"]

    def determine_bet(self):
        pass
    
    def tie_round(self):
        self.parent_player.money += self.current_bet
    
    def win_round(self):
        print("Player {} winning: {}".format(self.parent_player.name, self.current_bet*2))
        self.parent_player.money += 2 * self.current_bet

