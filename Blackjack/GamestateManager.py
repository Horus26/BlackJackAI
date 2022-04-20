from .CommandLinePlayer import CommandLinePlayer
from .SplitTempPlayer import SplitTempPlayer
from .Dealer import Dealer
from .Cards import Carddeck
from .GreedyAIPlayer import GreedyAIPlayer
from .Constants import PLAYER_ACTIONS
from secrets import choice

class GamestateManager :
    def __init__(self):
        self.player_list = []
        self.playable_carddeck = []
        self.current_playing_players = []
        self.dealer = Dealer()
        self.split_player_round_list = []
        self.minimum_bet = 1

    def init_game(self, player_objects_list, number_of_carddecks = 6, minimum_bet = 1):
        self.minimum_bet = minimum_bet if minimum_bet >= 1 else 1
        
        if number_of_carddecks < 1: number_of_carddecks = 1
        
        for i in range(number_of_carddecks):
            self.playable_carddeck.extend(Carddeck().deck)

        if len(player_objects_list) < 1: return False
        for player_object in player_objects_list:
            self.add_player(player_object)

        self.current_playing_players = list(self.player_list)
        return True


    def add_player(self, player_object):
        self.player_list.append(player_object)

    def remove_player(self, player):
        if player in self.player_list:
            print("Removing player: {}".format(player.name))
            self.player_list.remove(player)

    def print_playable_carddeck(self):
        for card in self.playable_carddeck:
            print(card)
        print("CARD COUNT: " + str(len(self.playable_carddeck)))

    # def start_game(self):
    #     self.play_round()
    #     self.clean_round()

    def init_round_cards(self):
        
        # # get bets from every player
        # for player in list(self.current_playing_players):
        #     valid_bet = False
        #     while(not valid_bet):
        #         bet = player.get_bet()
        #         if (isinstance(bet, int) or isinstance(bet, float)) and bet >= self.minimum_bet:
        #             player.current_bet = bet
        #             player.money -= bet
        #             valid_bet = True
        #         else:
        #             print("Invalid bet: {}".format(bet))

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

        self.print_gamestate()

    
    def print_gamestate(self):
        print("\nPrinting Gamestate")
        print("Dealer hand")
        self.dealer.print_hand()

        print("Player hands")
        for player in self.current_playing_players:
            player.print_hand()

        print()

    def deal_card_round(self):
        for player in self.current_playing_players:
            # draw random card
            card = self.get_random_card()
            # assign card to player
            player.add_card(card)

    def get_random_card(self):
        card = choice(self.playable_carddeck)
        self.playable_carddeck.remove(card)
        return card

    # TODO: REMOVE IF WORKING
    # def play_round(self):
    #     # check if dealer or a player has blackjack 
    #     dealer_blackjack = self.evaluate_dealt_cards()
    #     if dealer_blackjack: 
    #         return

    #     # player_round_values = []
    #     # ask each player for their turn
    #     # use self.player_list instead of self.current_playing_players as players can go bust in their turn and get removed from self.current_playing_players
    #     print("PLAYING ROUND")
    #     for player in self.player_list:
    #         # filter instant blackjack players
    #         if player.get_hand_value() == 21:
    #             continue

    #         print("\nPLAYERS TURN: {}".format(player.name))

    #         turn_value = self.player_turn(player)
    #         if turn_value > 21:
    #             # important that player can already lose here as it can affect other players
    #             print("Player {} bust".format(player.name))
    #             player.lose_round()
    #             self.current_playing_players.remove(player)
    #             continue
            
    #     self.dealer_turn()

    #     # Evaluate
    #     self.evaluate_round()

    def dealer_turn(self):
        # Dealer draw cards if hand value below 17
        while(self.dealer.make_turn()):
            self.dealer.add_card(self.get_random_card())

    def evaluate_dealt_cards(self):
        # get dealer hand value
        dealer_base_hand_value = self.dealer.get_hand_value()
        dealer_blackjack = True if dealer_base_hand_value == 21 else False
        if (dealer_blackjack):
            print("DEALER BLACKJACK")
            self.dealer.print_hand(second_card_visible=True)

        # get player hand values that are 21
        for player in self.player_list:
            player_blackjack = (player.get_hand_value() == 21)
            if dealer_blackjack and not player_blackjack:
                player.lose_round()
            elif dealer_blackjack and player_blackjack:
                player.tie_round()
            elif player_blackjack:
                player.dealt_cards_blackjack()
                self.current_playing_players.remove(player)


        return dealer_blackjack

            
    def get_valid_player_actions(self, player):
        valid_actions_list = [PLAYER_ACTIONS["Stand"]]
        
        # check if hit is valid (case where after splitting two aces only stand is valid)
        if player.check_hit_valid(): 
            valid_actions_list.append(PLAYER_ACTIONS["Hit"])

        # if hit not valid then split and double not valid aswell --> no valid check necessary
        else:
            return valid_actions_list
        
        print("CHECKING FOR SPLIT")
        # check if split is valid
        if player.check_split_valid(): valid_actions_list.append(PLAYER_ACTIONS["Split"])

        # check if double down is valid
        if player.check_double_valid(): valid_actions_list.append(PLAYER_ACTIONS["Double"])

        return valid_actions_list
    
    def player_turn(self, player, turn_action):               
        if turn_action == PLAYER_ACTIONS["Stand"]:
            return (True, None)

        turn_finished, split_player = self.execute_player_turn_action(player, turn_action)
        hand_value = player.get_hand_value()
        if hand_value > 21:
            # important that player can already lose here as it can affect other players
            print("Player {} bust".format(player.name))
            player.lose_round()
            if player in self.current_playing_players:
                self.current_playing_players.remove(player)
            else:
                self.split_player_round_list.remove(player)
            turn_finished = True
        elif hand_value == 21:
            turn_finished = True
        
        return turn_finished, split_player

    
    def execute_player_turn_action(self, player, turn_action):
        # evaluate turn
        if turn_action == PLAYER_ACTIONS["Hit"]: 
            self.hit(player)
            return(False, None)

        elif turn_action == PLAYER_ACTIONS["Double"]: 
            # after double down player gets one card and must stand after
            self.double(player)
            return (True, None)

        elif turn_action == PLAYER_ACTIONS["Split"]: 
            turn_finished, split_player = self.split(player)
            return (turn_finished, split_player)
        
        # else player action stand which results in no action (else case exists as emergency exit in case of failure)
        else: return (True, None)

    # def player_turn(self, player, turn_action, split_allowed = True):
    #         # get new hand value
    #         hand_value = player.get_hand_value()
    #         # check if player has no options left
    #         if hand_value >= 21: return hand_value
            
    #         # use while for waiting for a valid turn to reduce number of recursions
    #         valid_turn = False
    #         double_down = False
    #         while(not valid_turn):
    #             # ask player for turn action
    #             player_turn_action = player.make_turn()

    #             # evaluate turn
    #             if player_turn_action == PLAYER_ACTIONS["Hit"]: valid_turn = self.hit(player)
    #             elif player_turn_action == PLAYER_ACTIONS["Double"]: 
    #                 # after double down player gets one card and must stand after
    #                 valid_turn = self.double(player)
    #                 if valid_turn: return player.get_hand_value()

    #              # two seperate if statements because of else case
    #             elif player_turn_action == PLAYER_ACTIONS["Split"]: 
    #                 if split_allowed: valid_turn = self.split(player)
    #                 else: print("Resplitting not allowed")
    #                 if valid_turn: split_allowed = False
    #             # else player action stand which results in no action
    #             else: return player.get_hand_value()

            

    #         # recursion
    #         return self.player_turn(player, split_allowed)

    def hit(self, player):
        card = self.get_random_card()
        player.add_card(card)

        print("Player {} hit".format(player.name))
        player.print_hand()

    def double(self, player):        
        player.turn_double()
        print("{} doubling down".format(player.name))
        player.add_card(self.get_random_card())
        player.print_hand()

    def split(self, player):
        card = player.turn_split()

        # player turn with new hand
        split_temp_player = SplitTempPlayer(player, card)

        # add second card to original and split hand
        player.add_card(self.get_random_card())
        split_temp_player.add_card(self.get_random_card())

        # add new entry to split_player_round_dict for referencing split player in evaluation
        self.split_player_round_list.append(split_temp_player)

        # check if two aces were split -> then player must stand (no hit/split/double down allowed)
        # it does not matter whether the new hand is a blackjack
        if card.value == 1:
            split_temp_player.ace_counts += 1
            print("Aces were split --> player must stand")
            
            print("Player {} splitting".format(player.name))
            print("Splitted hand: ")
            split_temp_player.print_hand()
            print("Original new hand: ")
            player.print_hand()
            # turn finished
            return True, split_temp_player

        print("Player {} splitting".format(player.name))
        print("Splitted hand: ")
        split_temp_player.print_hand()
        print("Original new hand: ")
        player.print_hand()
        
        # player turn with original hand (that called split) not finished with turn
        return False, split_temp_player
        
    def evaluate_round(self):
        print("\nEVALUATION")
        dealer_hand_value = self.dealer.get_hand_value()
        print("Dealer hand value: {}".format(dealer_hand_value))
        self.dealer.print_hand(second_card_visible=True)

        # check if dealers busts and therefore all remaining players win
        if dealer_hand_value > 21:
            for player in self.current_playing_players + self.split_player_round_list:
                player.win_round()
        else:
            # check for every player against dealer
            for player in self.current_playing_players + self.split_player_round_list:
                hand_value = player.get_hand_value()
                print("\nPLAYER: {} has hand value: {}".format(player.name, hand_value))
                player.print_hand()
                
                if hand_value > 21:
                    player.lose_round()
                elif hand_value > dealer_hand_value:
                    player.win_round()
                elif hand_value == dealer_hand_value:
                    player.tie_round()
                else:
                    player.lose_round()


        if len(self.split_player_round_list) + len(self.current_playing_players) == 0:
            print("No players remaining that did not go bust")

        print()

    def clean_round(self):
        self.split_player_round_list.clear()
        for player in list(self.player_list):
            if player.money == 0 or player.money < self.minimum_bet:
                self.remove_player(player)
                print("Removed player: {}".format(player.name))
                continue
            print("{} money: {}".format(player.name, player.money))
            player.clear_cards()
        
        # prepare player list for next round
        self.current_playing_players = list(self.player_list)
        self.dealer.clear_cards()