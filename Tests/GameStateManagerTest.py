import unittest
from Blackjack.GamestateManager import GamestateManager
from Blackjack.GreedyAIPlayer import GreedyAIPlayer


class GamestateManagerTest(unittest.TestCase):

    def setUp(self):
        self.gamestate_manager = GamestateManager()
        player_list = []
        start_money = 34
        ai_player_name_list = ["Baek Jiheon", "Lee Nagyung", "Lee Chaeyoung"]
        for ai_player_name in ai_player_name_list:
            player_list.append(GreedyAIPlayer(ai_player_name, start_money))
        
        number_of_carddecks = 1
        self.gamestate_manager.init_game(player_list, number_of_carddecks)

    def test_init_game(self):
        # Assert
        self.assertEqual(len(self.gamestate_manager.player_list), 3)
        self.assertEqual(len(self.gamestate_manager.playable_carddeck), 52)
        
    
    def test_init_round(self):
        # check that bets are taken from every player and cards are dealt
        
        # Arrange
        player_money_before = []
        player_money_after = []
        carddeck_card_number = len(self.gamestate_manager.playable_carddeck)
        for player in self.gamestate_manager.player_list:
            player_money_before.append(player.money)

        # Act
        self.gamestate_manager.init_round()
        for player in self.gamestate_manager.player_list:
            player_money_after.append(player.money)

        # Assert
        for i, player in enumerate(self.gamestate_manager.player_list):
            self.assertEqual(player.current_bet, player_money_before[i] - player_money_after[i])
            self.assertEqual(len(player.cards), 2)

        self.assertEqual(len(self.gamestate_manager.dealer.cards), 2)
        self.assertEqual(len(self.gamestate_manager.playable_carddeck), carddeck_card_number - (len(self.gamestate_manager.player_list) + 1) * 2)
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()