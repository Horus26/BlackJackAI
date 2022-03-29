class Card :
    def __init__(self, _name, _value, _color):
        self.name = _name
        self.value = _value
        self.color = _color

    def __repr__(self):
        return "Card: {}, Value: {}, Color: {}".format(self.name, self.value, self.color)
