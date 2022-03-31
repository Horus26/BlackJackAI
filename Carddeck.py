from Card import Card
from Constants import COLORS


class Carddeck :
    def __init__(self):
        self.deck = []
        for color in COLORS:
            # add number cards
            for value in range(2, 11):
                self.deck.append(Card(color + str(value), value, color))
            # add image cards
            for i in ["J", "Q", "K"]:
                self.deck.append(Card(color + i, 10, color))
            # add ace 
            # TODO: WATCH OUT HANDLING ACE VALUE 11
            self.deck.append(Card(color + "A", 1, color))

    def printDeck(self):
        for card in self.deck:
            print(card)


if __name__ == "__main__":
    carddeck = Carddeck()
    carddeck.printDeck()