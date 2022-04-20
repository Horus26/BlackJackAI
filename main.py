from Blackjack.GUIPlayer import GUIPlayer
from Blackjack.GamestateManager import GamestateManager
from Blackjack.CommandLinePlayer import CommandLinePlayer
from Blackjack.GreedyAIPlayer import GreedyAIPlayer
from Blackjack.GUIGameView import GUIGameView
import arcade


def main():
    gamestate_manager = GamestateManager()
    
    # game settings
    gui = None
    player_list = []
    start_money = 34
    ai_player_name_list = ["Baek Jiheon", "Lee Nagyung", "Lee Chaeyoung", "Romsae", "Park Jiwon", "Jang Gyuri", "Roh Jisun", "Song Hayoung", "Lee Seoyeon"]
    for ai_player_name in ai_player_name_list:
        player_list.append(GreedyAIPlayer(ai_player_name, start_money))
    
    human_player = GUIPlayer("Human player", start_money)
    # human_player = CommandLinePlayer("Human player", start_money)
    player_list.append(human_player)

    # TODO: implement better solution for player init
    if not player_list:
        exit(34)

    gui = init_gui(player_list)

    valid_game = gamestate_manager.init_game(player_list)
    gui.gamestate_manager = gamestate_manager

    # start game with gui
    arcade.run()

    # play non gui game
    # play_non_gui_game(gamestate_manager)



def init_gui(player_list):
    window = arcade.Window(800, 600, "Blackjack")
    gui_game_view = GUIGameView()
    window.show_view(gui_game_view)
    gui_game_view.setup(player_list)
    return gui_game_view


def play_non_gui_game(gamestate_manager : GamestateManager):
    # handle initial bets
    for player in gamestate_manager.current_playing_players:
        valid_bet = False

        while(not valid_bet):

            bet = player.get_bet()

            if (isinstance(bet, int) or isinstance(bet, float)) and bet >= gamestate_manager.minimum_bet and bet <= player.money:
                player.current_bet = bet
                player.money -= bet
                valid_bet = True
            else:
                print("Invalid bet: {}".format(bet))     
    
    # deal out initial cards
    gamestate_manager.init_round_cards()
    
    # end round if dealer blackjack (win/lose per player already handled in evaluate dealt cards)
    dealer_blackjack = gamestate_manager.evaluate_dealt_cards()
    if dealer_blackjack:
        # TODO: BREAK AND START NEXT ROUND
        return

    # Players turn
    for player in list(gamestate_manager.current_playing_players):
        handle_player_turn(gamestate_manager, player)

    # dealer turn
    gamestate_manager.dealer_turn()

    # evaluate round
    gamestate_manager.evaluate_round()

def handle_player_turn(gamestate_manager : GamestateManager, player):
    hand_value = player.get_hand_value()
    
    turn_finished = False
    while(not turn_finished):
        if hand_value == 21:
            return

        turn_action = None
        valid_player_turn_actions = gamestate_manager.get_valid_player_actions(player)
        turn_action = player.make_turn()


        # check if chosen action is valid
        if turn_action not in valid_player_turn_actions:
            print("Invalid action: {}".format(turn_action))
            print("Valid actions were: ")
            print(*valid_player_turn_actions, sep=', ')
            continue

        # expected return values: true if turn is finished, false if not finished
        # finished turn when action was stand, double or player bust (hit > 21) or split with two aces
        turn_finished, split_player = gamestate_manager.player_turn(player, turn_action)

        if split_player is not None:
            handle_player_turn(gamestate_manager, split_player)


if __name__ == "__main__":
    main()