import unittest
from Blackjack.GamestateManager import GamestateManager


class GamestateManagerTest(unittest.TestCase):

    def setUp(self):
        self.gamestate_manager = GamestateManager()

    def test_init(self):
        # Arrange
        player_list = ["player1", "player2"]
        number_of_carddecks = 1
        
        # Act
        self.gamestate_manager.init_game(player_list, number_of_carddecks)

        # Assert
        self.assertEqual(len(self.gamestate_manager.player_list), 2)
        self.assertEqual(len(self.gamestate_manager.playable_carddeck), 52)

if __name__ == '__main__':
    unittest.main()