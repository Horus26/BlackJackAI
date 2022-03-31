from abc import ABC, abstractmethod

class Player(ABC) :
    def __init__(self, player_name, start_money):
        self.name = player_name
        self.money = start_money
        self.currentBet = 0
        self.cards = []
        self.ace_counts = 0

    def add_card(self, card):
        if(card.value == 1): self.ace_counts += 1
        self.cards.append(card)
    
    def clear_cards(self, card):
        self.cards.clear()
        self.ace_counts = 0
        self.currentBet = 0

    
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
        hand_value = temp_hand_value = sum([card.value for card in self.cards])
        
        # handling ace 1 / 11 cases
        for i in range(self.ace_counts):
            temp_hand_value += 10
            if temp_hand_value > 21: break
            hand_value = temp_hand_value
        
        return hand_value




