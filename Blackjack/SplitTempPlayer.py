from .Player import Player
from .Constants import PLAYER_ACTIONS

class SplitTempPlayer(Player) :
    def __init__(self, player, card):
        super(). __init__(player.name + "_split", 0)
        self.parent_player = player
        self.current_bet = player.currentBet
        self.cards.append(card)

    def make_turn(self):
        print("{} Hit".format(self.name))
        return PLAYER_ACTIONS["Hit"]

    def determine_bet(self):
        print("SplitTempPlayer {} determining bet".format(self.name))
        return 1
    
    def dealt_cards_blackjack(self):
        # blackjack after splitting does not count as direct dealt blackjack
        pass
