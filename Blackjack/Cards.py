from .Constants import COLORS

class Card :
    def __init__(self, _name, _value, _color, _image_value):
        self.name = _name
        self.value = _value
        self.color = _color
        self.image_value = _image_value

    def __repr__(self):
        return "Card: {}, Value: {}, Color: {}".format(self.name, self.value, self.color)


class Carddeck :
    def __init__(self):
        self.deck = []
        for color in COLORS:
            # add number cards
            for value in range(2, 11):
                self.deck.append(Card(color + str(value), value, color, value))
            # add image cards
            for i in ["J", "Q", "K"]:
                self.deck.append(Card(color + i, 10, color, i))
            # add ace as 1 and handle in player
            self.deck.append(Card(color + "A", 1, color, "A"))

    def printDeck(self):
        for card in self.deck:
            print(card)


if __name__ == "__main__":
    carddeck = Carddeck()
    carddeck.printDeck()