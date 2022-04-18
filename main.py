from Blackjack.GamestateManager import GamestateManager
from Blackjack.CommandLinePlayer import CommandLinePlayer
from Blackjack.GreedyAIPlayer import GreedyAIPlayer
from Blackjack.GUIGame import GUIGame

def main():
    gamestate_manager = GamestateManager()
    
    # game settings
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

    init_gui(player_list)

    # # start game
    # valid_game = gamestate_manager.init_game(player_list)
    # if(valid_game):
    #     # Check if human players want to play another round
    #     while(input("Play round? --> 'True': ") in ["True", "true"]):
    #         gamestate_manager.start_game()


def init_gui(player_list):
    game = GUIGame(800, 600, "Blackjack")
    game.setup(player_list)
    game.start_gui()



if __name__ == "__main__":
    main()