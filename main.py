from Blackjack.GamestateManager import GamestateManager
from Blackjack.CommandLinePlayer import CommandLinePlayer
from Blackjack.GreedyAIPlayer import GreedyAIPlayer
from Blackjack.GUIGame import GUIGame


def main():
    gamestate_manager = GamestateManager()
    
    # game settings
    gui = None
    player_list = []
    start_money = 34
    ai_player_name_list = ["Baek Jiheon", "Lee Nagyung", "Lee Chaeyoung", "Romsae", "Park Jiwon", "Jang Gyuri", "Roh Jisun", "Song Hayoung", "Lee Seoyeon"]
    for ai_player_name in ai_player_name_list:
        player_list.append(GreedyAIPlayer(ai_player_name, start_money))
    
    human_player = CommandLinePlayer("Human player", start_money)
    player_list.append(human_player)

    # TODO: implement better solution for player init
    if not player_list:
        exit(34)

    # gui = init_gui(player_list)

    # start game
    valid_game = gamestate_manager.init_game(player_list)

    # connect gui with gamestate manager
    if gui is not None: gui.gamestate_manager = gamestate_manager

    play_game(gamestate_manager, gui)
    # if(valid_game):
    #     # Check if human players want to play another round
    #     while(input("Play round? --> 'True': ") in ["True", "true"]):
    #         gamestate_manager.start_game()


def init_gui(player_list):
    game_gui = GUIGame(800, 600, "Blackjack")
    game_gui.setup(player_list)
    game_gui.start_gui()
    return game_gui

def play_game(gamestate_manager : GamestateManager, gui : GUIGame):
    # handle initial bets
    for player in gamestate_manager.current_playing_players:
        valid_bet = False
        while(not valid_bet):
            bet = player.get_bet()
            if (isinstance(bet, int) or isinstance(bet, float)) and bet >= gamestate_manager.minimum_bet:
                player.current_bet = bet
                player.money -= bet
                valid_bet = True
            else:
                print("Invalid bet: {}".format(bet))     
    
    # deal out initial cards
    gamestate_manager.init_round_cards()
    
    # # TODO: DEBUG ENTFERNEN
    # # create two cards with value 5 to test all player actions
    # from Blackjack.Cards import Card
    # from Blackjack.Constants import COLOR_SPADE
    # card1 = Card(COLOR_SPADE + str(5), 5, COLOR_SPADE, 5)
    # card2 = Card(COLOR_SPADE + str(5), 5, COLOR_SPADE, 5)
    # gamestate_manager.player_list[-1].cards.clear()
    # gamestate_manager.player_list[-1].cards = [card1, card2]
    
    # TODO: deal out cards at gui level aswell


    # end round if dealer blackjack (win/lose per player already handled in evaluate dealt cards)
    dealer_blackjack = gamestate_manager.evaluate_dealt_cards()
    if dealer_blackjack:
        # TODO: BREAK AND START NEXT ROUND
        pass

    # Players turn
    for player in list(gamestate_manager.current_playing_players):
        handle_player_turn(gamestate_manager, player, gui)

    # dealer turn
    gamestate_manager.dealer_turn()

    # evaluate round
    gamestate_manager.evaluate_round()

def handle_player_turn(gamestate_manager : GamestateManager, player, gui : GUIGame):
    hand_value = player.get_hand_value()
    
    turn_finished = False
    while(not turn_finished):
        if hand_value == 21:
            return

        turn_action = None
        valid_player_turn_actions = gamestate_manager.get_valid_player_actions(player)
        if gui is None:
            turn_action = player.make_turn()
        else:
            # TODO: GET ACTION FROM GUI
            pass

        # check if chosen action is valid
        if turn_action not in valid_player_turn_actions:
            print("Invalid action: {}".format(turn_action))
            print("Valid actions were: ")
            print(*valid_player_turn_actions, sep=', ')
            continue

        # expected return values: true if turn is finished, false if not finished
        # finished turn when action was stand, double or player bust (hit > 21) or split with two aces
        (turn_finished, hand_value, split_player) = gamestate_manager.player_turn(player, turn_action)
        if hand_value > 21:
            # important that player can already lose here as it can affect other players
            print("Player {} bust".format(player.name))
            player.lose_round()
            if player in gamestate_manager.current_playing_players:
                gamestate_manager.current_playing_players.remove(player)
            else:
                gamestate_manager.split_player_round_list.remove(player)
            turn_finished = True

        if split_player is not None:
            handle_player_turn(gamestate_manager, split_player, gui)


if __name__ == "__main__":
    main()