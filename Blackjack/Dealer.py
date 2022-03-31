from .Player import Player

class Dealer(Player) :
    def __init__(self):
        super(). __init__("Dealer", 0)

    def make_turn(self):
        return (self.get_hand_value() < 17)

    def determine_bet(self):
        pass