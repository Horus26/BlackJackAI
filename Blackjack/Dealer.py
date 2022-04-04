from .Player import Player

class Dealer(Player) :
    def __init__(self):
        super(). __init__("Dealer", 0)

    def make_turn(self):
        return (self.get_hand_value() < 17)

    def determine_bet(self):
        pass

    def print_hand(self, second_card_visible = False):
        print("Hand from {}".format(self.name))
        if second_card_visible:
            print(*[card.name for card in self.cards], sep=", ")
            print("Hand value: {}\n".format(self.get_hand_value()))
        else:
            print(self.cards[0].name)