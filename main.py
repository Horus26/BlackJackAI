from Blackjack.GamestateManager import GamestateManager
from Blackjack.CommandLinePlayer import CommandLinePlayer
from Blackjack.GreedyAIPlayer import GreedyAIPlayer


def main():
    gamestate_manager = GamestateManager()
    # self.player_list.append(CommandLinePlayer("Human player", 34))
    
    player_list = []
    start_money = 34
    ai_player_name_list = ["Baek Jiheon", "Lee Nagyung", "Lee Chaeyoung"]
    for ai_player_name in ai_player_name_list:
        player_list.append(GreedyAIPlayer(ai_player_name, start_money))
    
    human_player = CommandLinePlayer("Human player", start_money)
    player_list.append(human_player)

    valid_game = gamestate_manager.init_game(player_list)
    if(valid_game):
        # Check if human players want to play another round
        while(input("Play round? --> 'True': ") in ["True", "true"]):
            gamestate_manager.start_game()

if __name__ == "__main__":
    main()