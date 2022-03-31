from abc import ABC, abstractmethod
from Constants import PLAYER_ACTIONS

class Player(ABC) :
    def __init__(self, player_name, start_money):
        self.name = player_name
        self.money = start_money
        self.currentBet = 0
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
    
    def clear_cards(self, card):
        self.cards.clear()

    
    def get_bet(self):
        bet = self.determine_bet()
        while(bet is not None and bet > self.money): 
            bet = self.determine_bet()
        
        if bet is not None:
            self.money -= bet
            
        self.currentBet = bet
        return bet

    @abstractmethod
    def determine_bet(self):
        pass

    @abstractmethod
    def make_turn(self):
        pass

    def get_hand_value(self):
        return sum([card.value for card in self.cards])




