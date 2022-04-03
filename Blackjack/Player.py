from abc import ABC, abstractmethod

class Player(ABC) :
    def __init__(self, player_name, start_money):
        self.name = player_name
        self.money = start_money
        self.current_bet = 0
        self.cards = []
        self.ace_counts = 0

    def add_card(self, card):
        if(card.value == 1): self.ace_counts += 1
        self.cards.append(card)
    
    def clear_cards(self):
        self.cards.clear()
        self.ace_counts = 0
        self.current_bet = 0

    
    def get_bet(self):
        bet = self.determine_bet()
        while(bet is not None and bet > self.money): 
            bet = self.determine_bet()
        
        if bet is not None:
            self.money -= bet
            
        self.current_bet = bet
        return bet

    @abstractmethod
    def determine_bet(self):
        pass

    @abstractmethod
    def make_turn(self):
        pass

    def get_hand_value(self):
        # find best sum of cards in hand that is below 21 if possible
        hand_value = temp_hand_value = sum([card.value for card in self.cards])
        
        # handling ace 1 / 11 cases
        for i in range(self.ace_counts):
            temp_hand_value += 10
                
            if temp_hand_value > 21: break
            hand_value = temp_hand_value
        
        return hand_value

    def print_hand(self):
        print("Printing hand from {}".format(self.name))
        print(*[card.name for card in self.cards], sep=", ")

    def lose_round(self):
        print("Player {} losing: {}".format(self.name, self.current_bet))
        self.clear_cards()
    
    def tie_round(self):
        print("Player {} tie --> keeping bet: {}".format(self.name, self.current_bet))
        self.money += self.current_bet
        self.clear_cards()

    def dealt_cards_blackjack(self):
        print("Player {} instant blackjack --> winning: {}".format(self.name, self.current_bet*2.5))
        self.money += round(self.current_bet * 1.5, 2)
        self.clear_cards()
    
    def win_round(self):
        print("Player {} winning: {}".format(self.name, self.current_bet*2))
        self.money += 2 * self.current_bet
        self.clear_cards()

    def init_split(self):
        # check if all requirements are fullfilled for split
        if self.money < self.current_bet or len(self.cards) != 2 or self.cards[0].value != self.cards[1].value:
            return (False, None)
        else:
            self.money -= self.current_bet
            card = self.cards[1]
            self.cards.remove(card)
            return (True, card)




