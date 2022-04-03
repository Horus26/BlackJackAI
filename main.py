from Blackjack.GamestateManager import GamestateManager


def main():
    gamestate_manager = GamestateManager()
    gamestate_manager.init_game(["Baek Jiheon", "Lee Nagyung", "Lee Chaeyoung"], 3)
    gamestate_manager.start_game()
    gamestate_manager.start_game()
    gamestate_manager.start_game()
    gamestate_manager.start_game()

if __name__ == "__main__":
    main()