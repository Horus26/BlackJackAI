from .Dealer import Dealer
from .Cards import Carddeck
from .GreedyAIPlayer import GreedyAIPlayer
from .Constants import PLAYER_ACTIONS
from secrets import choice

class GamestateManager :
    def __init__(self, ):
        self.player_list = []
        self.playable_carddeck = []
        self.current_player = None
        self.dealer = Dealer()

    def init_game(self, player_names_list = ["Player_1"], number_of_carddecks = 1):
        if number_of_carddecks < 1: number_of_carddecks = 1
        
        for i in range(number_of_carddecks):
            self.playable_carddeck.extend(Carddeck().deck)

        if len(player_names_list) < 1: player_names_list = ["Player_1"]
        for player_name in player_names_list:
            self.add_player(player_name)

    
    def add_player(self, player_name):
        self.player_list.append(GreedyAIPlayer(player_name, 34))

    def remove_player(self, player):
        if player in self.player_list:
            self.player_list.remove(player)

    def print_playable_carddeck(self):
        for card in self.playable_carddeck:
            print(card)
        print("CARD COUNT: " + str(len(self.playable_carddeck)))

    def start_game(self):
        self.init_round()
        self.play_round()

    def init_round(self):
        # get bets from every player
        for player in self.player_list:
            bet = player.get_bet()
            if bet is None: 
                self.player_list.remove(player)

        # deal one card each to every player
        self.deal_card_round()

        # then one card to the dealer
        dealerCard = self.get_random_card()
        self.dealer.add_card(dealerCard)

        # then the second card to every player
        self.deal_card_round()

        # then a face down second card to the dealer
        secondDealerCard = self.get_random_card()
        self.dealer.add_card(secondDealerCard)
        
    
    def deal_card_round(self):
        for player in self.player_list:
            # draw random card
            card = self.get_random_card()
            # assign card to player
            player.add_card(card)

    def get_random_card(self):
        card = choice(self.playable_carddeck)
        self.playable_carddeck.remove(card)
        return card

    def play_round(self):
        player_round_values = []
        # ask each player for their turn
        for player in self.player_list:
            turn_value = self.player_turn(player)
            player_round_values.append(turn_value)

        # Dealer draw cards if hand value below 17
        while(self.dealer.make_turn()):
            self.dealer.add_card(self.get_random_card())

        # Evaluate
        self.evaluate_round(player_round_values)



    def player_turn(self, player):
            # get new hand value
            hand_value = player.get_hand_value()
            
            # check if player has no options left
            if hand_value >= 21 or player.money == 0: return hand_value
            
            player_turn_action = player.make_turn()

            # get new hand value
            hand_value = player.get_hand_value()

            # evaluate turn
            if player_turn_action == PLAYER_ACTIONS["Hit"]: self.hit(player)
            elif player_turn_action == PLAYER_ACTIONS["Double"]: self.double(player)
            elif player_turn_action == PLAYER_ACTIONS["Split"]: self.split(player)
            # else player action stand which results in no action
            else: return hand_value


            
            # recursion
            return self.player_turn(player)

    def hit(self, player):
        card = self.get_random_card()
        player.add_card(card)

    def double(self):
        # TODO:
        pass

    def split(self):
        # TODO:
        pass

    def evaluate_round(self, player_round_values):
        # TODO: evaluate winners
        for i, hand_value in enumerate(player_round_values):
            print("PLAYER: {} has hand value: {}".format(self.player_list[i].name, hand_value))
            for card in self.player_list[i].cards: print("Player card: {}".format(card.name))

        print("Dealer cards")
        for card in self.dealer.cards: print("Dealer card: {}".format(card.value))
        print("Dealer hand value: {}".format(self.dealer.get_hand_value()))
