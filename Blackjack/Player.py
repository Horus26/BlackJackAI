from abc import ABC, abstractmethod

class Player(ABC) :
    def __init__(self, player_name, start_money):
        self.name = player_name
        self.money = start_money
        self.current_bet = 0
        self.cards = []
        self.ace_counts = 0
        # resplitting not allowed
        self.split_this_round = False
        self.gui_player = False

    def add_card(self, card):
        if(card.value == 1): self.ace_counts += 1
        self.cards.append(card)
    
    def clear_cards(self):
        self.cards.clear()
        self.ace_counts = 0
        self.current_bet = 0
        self.split_this_round = False

    
    def get_bet(self):
        bet = self.determine_bet()
        while(bet is None): 
            bet = self.determine_bet()
        
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
        print("Hand from {}".format(self.name))
        print(*[card.name for card in self.cards], sep=", ")
        print("Hand value: {}\n".format(self.get_hand_value()))

    def lose_round(self):
        print("Player {} losing bet: {}".format(self.name, self.current_bet))
        self.current_bet = 0
        # self.clear_cards()
    
    def tie_round(self):
        print("Player {} tie --> keeping bet: {}".format(self.name, self.current_bet))
        win = self.current_bet
        self.money += win
        self.clear_cards()
        return win
        

    def dealt_cards_blackjack(self):
        print("Player {} instant blackjack --> winning: {}".format(self.name, self.current_bet*2.5))
        win = round(self.current_bet * 2.5, 2)
        self.money += win
        self.current_bet = 0
        return win
    
    def win_round(self):
        print("Player {} winning: {}".format(self.name, self.current_bet*2))
        win = (2 * self.current_bet)
        self.money += win
        self.clear_cards()
        return win

    def check_hit_valid(self):
        if (self.split_this_round and self.cards[0].value == 1) or (self.get_hand_value == 21 and self.ace_counts == 0):
            return False
        return True

    def check_split_valid(self):
        # check if all requirements are fullfilled for split
        if self.split_this_round or self.money < self.current_bet or len(self.cards) != 2 or self.cards[0].image_value != self.cards[1].image_value:
            return False
        return True
        # else:
        #     self.money -= self.current_bet
        #     card = self.cards[1]
        #     self.cards.remove(card)
        #     return (True, card)
    
    def turn_split(self):
        self.split_this_round = True
        self.money -= self.current_bet
        card = self.cards[1]
        self.cards.remove(card)
        return card

    def check_double_valid(self):
        # double down currently allowed after splitting
 
        # check for cards dealt total of 9, 10 or 11
        double_total_allowed = False
        temp_hand_value = sum([card.value for card in self.cards])
        if temp_hand_value in [9,10,11]: 
            double_total_allowed = True
        else:
            # handling ace 1 / 11 cases
            for i in range(self.ace_counts):
                temp_hand_value += 10   
                if temp_hand_value in [9,10,11]: 
                    double_total_allowed = True
                    break

        # only allow doubling down if there is enough money and cards dealt total is 9, 10 or 11 
        if self.money < self.current_bet or not double_total_allowed:
            return False

        return True
    
    def turn_double(self):
        self.money -= self.current_bet
        self.current_bet *= 2




