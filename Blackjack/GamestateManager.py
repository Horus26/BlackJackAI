from posixpath import split
from .SplitTempPlayer import SplitTempPlayer
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
        self.split_player_round_dict = {}

    def init_game(self, player_names_list = ["Player_1"], number_of_carddecks = 6):
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
        for player in list(self.player_list):
            bet = player.get_bet()
            if bet is None: 
                self.remove_player(player)

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
        # check if dealer or a player has blackjack 
        dealer_blackjack = self.evaluate_dealt_cards()
        if dealer_blackjack: return

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

    def evaluate_dealt_cards(self):
        # get dealer hand value
        dealer_base_hand_value = self.dealer.get_hand_value()
        dealer_blackjack = True if dealer_base_hand_value == 21 else False

        # get player hand values that are 21
        for player in self.player_list:
            player_blackjack = player.get_hand_value() == 21
            if dealer_blackjack and not player_blackjack:
                player.lose_round()
            elif dealer_blackjack and player_blackjack:
                player.tie_round()
            elif player_blackjack:
                player.dealt_cards_blackjack()


        return dealer_blackjack

            

    def player_turn(self, player, split_allowed = True):
            # get new hand value
            hand_value = player.get_hand_value()
            
            # check if player has no options left
            if hand_value >= 21 or player.money == 0: return hand_value
            
            # use while for waiting for a valid turn to reduce number of recursions
            valid_turn = False
            while(not valid_turn):
                # ask player for turn action
                player_turn_action = player.make_turn()

                # evaluate turn
                if player_turn_action == PLAYER_ACTIONS["Hit"]: valid_turn = self.hit(player)
                elif player_turn_action == PLAYER_ACTIONS["Double"]: valid_turn = self.double(player)
                 # two seperate if statements because of else case
                elif player_turn_action == PLAYER_ACTIONS["Split"]: 
                    if split_allowed: valid_turn = self.split(player)
                # else player action stand which results in no action
                else: return player.get_hand_value()

            # recursion
            return self.player_turn(player)

    def hit(self, player):
        card = self.get_random_card()
        player.add_card(card)
        return True

    def double(self, player):
        # TODO:
        pass

    def split(self, player):
        (valid, card) = player.init_split()
        if not valid: return False

        # player turn with new hand
        split_temp_player = SplitTempPlayer(player, card)
        
        # add second card to original and split hand
        player.add_card(self.get_random_card())
        split_temp_player.add_card(self.get_random_card())

        # add new entry to split_player_round_dict for referencing split player in evaluation
        #  TODO: USE IN EVALUATION
        self.split_player_round_dict[str(self.player_list.index(player))] = split_temp_player

        # check if two aces were split -> then player must stand (no hit/split/double down allowed)
        # it does not matter whether the new hand is a blackjack
        if card.value == 1:
            return True
        # else hit and double down allowed
        else:
            self.player_turn(split_temp_player, split_allowed=False)


        # finish player turn with original hand
        
        return True
        # TODO: FINISH


    def evaluate_round(self, player_round_values):
        # TODO: evaluate winners
        for i, hand_value in enumerate(player_round_values):
            print("PLAYER: {} has hand value: {}".format(self.player_list[i].name, hand_value))
            self.player_list[i].print_hand()
            
            # check if player was already paid in case of an instant blackjack with two cards
            if hand_value == 21 and len(self.player_list[i].cards) == 2:
                continue

            # TODO: Cash out

        print()
        print("Dealer hand value: {}".format(self.dealer.get_hand_value()))
        self.dealer.print_hand()

        # # TODO: outsource to clean up
        self.split_player_round_dict.clear()