import math
from posixpath import split
import arcade
import arcade.gui
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton
from Blackjack.Constants import PLAYER_ACTIONS
from Blackjack.GamestateManager import GamestateManager
from .GUIConstants import get_gui_constants, VERTICAL_MARGIN_PERCENT, CARD_SUITS, CARD_VALUES
from .GUICard import GUICard



class GUIGameView(arcade.View):

    def __init__(self, width = 800, height = 600, title = "Blackjack"):
        # super().__init__(width, height, title)
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        self.ui_manager = UIManager()

        # Sprite list for cards (used for drawing all cards)
        self.card_list = None
        # dict for easier manipulation of existing cards (relevant for moving cards in case of split)
        self.card_dict_data_access = None

        # list holding a list of cards for every player
        self.player_mats_list = None
        self.split_player_mats_dict = None

        # Sprite list for places where cards can be placed (mats) (used for drawing all mats)
        self.pile_mat_list = None

        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.TITLE = title

        self.MAT_WIDTH = None
        self.MAT_HEIGHT = None
        self.MAT_X_OFFSET = None

        # reference to gamestate manager
        self.gamestate_manager : GamestateManager = None

        self.DEFAULT_FONT_SIZE = 60

        self.game_phase = 0
        self.input_active = False
        self.active_player_index = 0
        self.send_input = False
        self.v_box = None
        self.ui_input_box = None
        self.NUMBER_OF_HANDS_PER_SIDE = 0
        self.CARD_SCALE = 1
        self.turn_option_box = None
        self.split_player = None
        self.gui_turn_action = None
        self.results_widget_box = None

    def setup(self, player_list):
        """ Set up the game variables. Call to re-start the game. """
        self.ui_manager.clear()
        self.ui_manager.enable()
        
        self.game_phase = 0
        self.active_player_index = 0
        # (reset) card list
        self.card_list = arcade.SpriteList()
        self.card_dict_data_access = {}
        # (reset) Sprite list with all the mats that cards lay on
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()
        # reset gamestate manager
        if self.gamestate_manager is not None:
            self.gamestate_manager.clean_round()

        if not player_list:
            raise RuntimeError("There were no players specified") 
        
        self.player_list = player_list
        self.player_text_list = []
        # prepare a list for every player (for convenient access and adding of mats)
        self.player_mats_list = [[] for _ in range(len(player_list)+1)]
        self.split_player_mats_dict = {}

        # prepare settings for displaying
        self.NUMBER_OF_HANDS_PER_SIDE = math.ceil(len(self.player_list) / 2)
        print("PLAYER COUNT: {}".format(len(self.player_list)))
        (self.CARD_SCALE, self.MAT_HEIGHT, self.MAT_WIDTH, self.MAT_X_OFFSET, MAT_Y_OFFSET, BOTTOM_Y, TOP_Y, START_X) = get_gui_constants(self.NUMBER_OF_HANDS_PER_SIDE, self.SCREEN_HEIGHT)
        print("NUMBER_OF_HANDS_PER_SIDE: {}".format(self.NUMBER_OF_HANDS_PER_SIDE))
        

        # draw player names, dealer name and according mats for cards
        self.DEFAULT_FONT_SIZE = 60 * self.CARD_SCALE
        x_start_position = START_X
        x_text_name_position = x_start_position - self.MAT_WIDTH / 2
        text_anchor_x = "left"
        row_index = 0

        # prepare for drawing dealer name
        self.player_text_list.append(arcade.Text(
            "Dealer",
            self.SCREEN_WIDTH/2 - self.MAT_WIDTH / 2,
            TOP_Y + 2*VERTICAL_MARGIN_PERCENT * self.MAT_HEIGHT + self.MAT_HEIGHT * 1.5,
            arcade.color.BLACK,
            self.DEFAULT_FONT_SIZE,
            anchor_x = "center"
            ))

        # prepare dealer start hand mats
        for j in range(2):
            pile = arcade.SpriteSolidColor(self.MAT_WIDTH, self.MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = self.SCREEN_WIDTH/2 - self.MAT_X_OFFSET + j * self.MAT_X_OFFSET, TOP_Y + 2*VERTICAL_MARGIN_PERCENT * self.MAT_HEIGHT + self.MAT_HEIGHT
            self.pile_mat_list.append(pile)
            # ! dealer is placed at position 0 for convenience !
            self.player_mats_list[0].append(pile)

        x_offset = self.MAT_X_OFFSET
        for i in range(len(self.player_list)):

            # prepare for drawing player names
            if i > self.NUMBER_OF_HANDS_PER_SIDE-1:
                x_text_name_position =  x_start_position + 0.5 * self.MAT_WIDTH + x_offset
                text_anchor_x = "right"
            self.player_text_list.append(arcade.Text(
                "{} ({})".format(self.player_list[i].name, self.player_list[i].money),
                start_x = x_text_name_position,
                start_y = TOP_Y - row_index * MAT_Y_OFFSET + self.MAT_HEIGHT / 2,
                color = arcade.color.BLACK,
                font_size = self.DEFAULT_FONT_SIZE,
                anchor_x = text_anchor_x
                ))

            # prepare start hand mats (2) for every player
            for j in range(2):
                pile = arcade.SpriteSolidColor(self.MAT_WIDTH, self.MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
                pile.position = x_start_position + j * x_offset, TOP_Y - row_index * MAT_Y_OFFSET
                self.pile_mat_list.append(pile)
                self.player_mats_list[i+1].append(pile)
            

            print("INDEX I: {}".format(i))
            print("X POS: {}, Y POS: {}".format(x_start_position, TOP_Y - row_index * MAT_Y_OFFSET))
            
            # handle different positioning depending on index of player
            if i >= self.NUMBER_OF_HANDS_PER_SIDE-1:
                x_start_position = self.SCREEN_WIDTH - START_X
                x_offset = -self.MAT_X_OFFSET
                if i >= self.NUMBER_OF_HANDS_PER_SIDE:
                    row_index -= 1
            else:
                row_index += 1

        # Create every card
        # for card_suit in CARD_SUITS:
        #     counter = 0
        #     for card_value in CARD_VALUES:
        #         card = GUICard(card_suit, card_value, CARD_SCALE)
        #         card.position = START_X + counter * MAT_X_OFFSET, TOP_Y + 2*VERTICAL_MARGIN_PERCENT * MAT_HEIGHT + MAT_HEIGHT
        #         self.card_list.append(card)
        #         # counter += 1
        # card = GUICard("Back_green", "5", self.CARD_SCALE)
        # card.position = START_X, TOP_Y + 2*VERTICAL_MARGIN_PERCENT * self.MAT_HEIGHT + self.MAT_HEIGHT
        # self.card_list.append(card)


        # prepare ui box for player bet input
        # region 
        # Create a text label
        label = arcade.gui.UILabel(
            text="Enter bet",
            text_color=arcade.color.DARK_RED,
            font_size=self.DEFAULT_FONT_SIZE*2,
            font_name="Kenney Future")
        
        # Create a button
        submit_button = UIFlatButton(
            color=arcade.color.DARK_BLUE_GRAY,
            text='Submit')

        @submit_button.event("on_click")    
        def on_click_submit(self, event):
            self.send_input = True
        
        self.ui_input_box = arcade.gui.UIInputText(
             width=self.DEFAULT_FONT_SIZE * 10,
             height=self.DEFAULT_FONT_SIZE,
             text="Set bet"
         )

        self.ui_input_box.cursor_index = len(self.ui_input_box.text)
        self.v_box = UIBoxLayout(
            children=[label, self.ui_input_box, submit_button]
        )
        # endregion

        # prepare ui box for player turn options
        # region
        self.turn_option_box = arcade.gui.UIBoxLayout()

        label = arcade.gui.UILabel(
            text="Choose turn action",
            text_color=arcade.color.DARK_RED,
            font_size=self.DEFAULT_FONT_SIZE*2,
            font_name="Kenney Future")

        # Create four buttons as there are four turn options for a player
        options = ["Hit", "Stand", "Double", "Split"]
        
        option_button = UIFlatButton(
            color=arcade.color.DARK_BLUE_GRAY,
            text=options[0])
        # Handle Clicks
        @option_button.event("on_click")
        def on_click_flatbutton(event):
            self.gui_turn_action = PLAYER_ACTIONS[options[0]]
            self.send_input = True
            print("GUI TURN ACTION: {}, {}".format(options[0], self.gui_turn_action))
        self.turn_option_box.add(option_button)
        
        option_button_1 = UIFlatButton(
            color=arcade.color.DARK_BLUE_GRAY,
            text=options[1])
        # Handle Clicks
        @option_button_1.event("on_click")
        def on_click_flatbutton(event):
            self.gui_turn_action = PLAYER_ACTIONS[options[1]]
            self.send_input = True
            print("GUI TURN ACTION: {}, {}".format(options[1], self.gui_turn_action))
        self.turn_option_box.add(option_button_1)
        
        option_button_2 = UIFlatButton(
            color=arcade.color.DARK_BLUE_GRAY,
            text=options[2])
        # Handle Clicks
        @option_button_2.event("on_click")
        def on_click_flatbutton(event):
            self.gui_turn_action = PLAYER_ACTIONS[options[2]]
            self.send_input = True
            print("GUI TURN ACTION: {}, {}".format(options[2], self.gui_turn_action))
        self.turn_option_box.add(option_button_2)
        
        option_button_3 = UIFlatButton(
            color=arcade.color.DARK_BLUE_GRAY,
            text=options[3])
        # Handle Clicks
        @option_button_3.event("on_click")
        def on_click_flatbutton(event):
            self.gui_turn_action = PLAYER_ACTIONS[options[3]]
            self.send_input = True
            print("GUI TURN ACTION: {}, {}".format(options[3], self.gui_turn_action))
        self.turn_option_box.add(option_button_3)

        self.turn_option_box.add(label)
        # endregion

        # prepare widget for displaying results
        # region
        self.results_widget_box = arcade.gui.UIBoxLayout()

        label = arcade.gui.UILabel(
            text="Results",
            text_color=arcade.color.DARK_RED,
            font_size=self.DEFAULT_FONT_SIZE*2,
            font_name="Kenney Future")

        results_text = arcade.gui.UITextArea(
        text="",
        height=300,
        text_color=arcade.color.DARK_RED,
        font_size=self.DEFAULT_FONT_SIZE,
        font_name="Kenney Future",
        size_hint_min=(400, 300)
        )    

        self.results_widget_box.add(label)
        self.results_widget_box.add(results_text)
        # endregion


       


    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Call draw() on all your sprite lists below
        self.card_list.draw()

        # draw text
        for text in self.player_text_list:
            text.draw()
        
        self.ui_manager.draw()
        

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.game_phase == 1:
            self.bet_phase()
        elif self.game_phase == 2:
            self.deal_cards_phase()
        elif self.game_phase == 3:
            self.player_turn_phase()
        elif self.game_phase == 4:
            self.dealer_phase()
        elif self.game_phase == 5:
            self.evaluation_phase()


    def bet_phase(self):
        if self.active_player_index is None:
            self.active_player_index = 0
            self.game_phase += 1
            print("BET PHASE FINISHED")
            return

        current_player = self.player_list[self.active_player_index]

        if current_player.gui_player:
            if self.input_active == False:
                self.add_bet_input_field_widget()
            else:
                bet = self.ui_input_box.text
                # print("UI TEXT: {}".format(gui_input))
                
                if not self.send_input:
                    return
                
                try:
                    bet = float(bet)
                except ValueError:
                    print ("Error: '{}' is not a valid float!".format(bet))
                    self.send_input = False
                    return

                if  self.check_bet_input_valid(bet, current_player):
                    self.player_text_list[self.active_player_index+1].text = "{} ({}): {}".format(self.player_list[self.active_player_index].name, self.player_list[self.active_player_index].money, bet)
                    if self.active_player_index+1 > self.NUMBER_OF_HANDS_PER_SIDE-1:
                        x_offset_gui_player = -(len(str(bet)) + 2)
                        self.player_text_list[self.active_player_index+1].x += x_offset_gui_player
                    
                    self.active_player_index += 1
                
                self.send_input = False
        else:
            if self.input_active:
                self.remove_widgets()
            else:
                bet = current_player.get_bet()
                if self.check_bet_input_valid(bet, current_player):
                    self.player_text_list[self.active_player_index+1].text = "{} ({}): {}".format(self.player_list[self.active_player_index].name, self.player_list[self.active_player_index].money, bet)
                    if self.active_player_index+1 > self.NUMBER_OF_HANDS_PER_SIDE-1:
                        x_offset_gui_player = -(len(str(bet)) + 2)
                        self.player_text_list[self.active_player_index+1].x += x_offset_gui_player
                    
                    self.active_player_index += 1

        if self.active_player_index == len(self.player_list):
            self.active_player_index = None
            self.remove_widgets()

    def check_bet_input_valid(self, bet, player):
        valid_bet = False
        if (isinstance(bet, int) or isinstance(bet, float)) and bet >= self.gamestate_manager.minimum_bet and bet <= player.money:
            player.current_bet = bet
            player.money -= bet
            valid_bet = True
        else:
            print("Invalid bet: {}".format(bet))   
        return valid_bet

    def deal_cards_phase(self):
        self.gamestate_manager.init_round_cards()
        
        # DEBUG TO TEST SPLIT
        from Blackjack.Cards import Card
        test_cards = []
        for test_card in self.gamestate_manager.playable_carddeck:
            if test_card.unique_id in ["0SpadesJ", "0HeartsJ"]:
                test_cards.append(test_card)
        self.gamestate_manager.player_list[-1].cards = test_cards
        # self.gamestate_manager.player_list[-1].ace_counts = 1
        self.gamestate_manager.player_list[-1].print_hand()
        
        # start from index 1 to handle dealer seperately
        for i in range(1, len(self.player_list)+1):
            cards =  self.player_list[i-1].cards
            # create first card at correct position
            GUI_card = GUICard(cards[0].color_string, cards[0].image_value, self.CARD_SCALE)
            GUI_card.position = self.player_mats_list[i][0].position
            self.card_list.append(GUI_card)
            # add card to dict to identify it later correctly
            self.card_dict_data_access[cards[0].unique_id] = GUI_card
            # create second card at correct position
            GUI_card = GUICard(cards[1].color_string, cards[1].image_value, self.CARD_SCALE)
            GUI_card.position = self.player_mats_list[i][1].position
            self.card_list.append(GUI_card)
            self.card_dict_data_access[cards[1].unique_id] = GUI_card
        
        # DEBUG TO TEST DEALER BLACKJACK
        # from Blackjack.Cards import Card
        # self.gamestate_manager.dealer.cards = [Card(u'\u2660' + "J", 10, u'\u2660', "J", "Spades"), Card(u'\u2660' + "A", 1, u'\u2660', "A", "Spades")]
        # self.gamestate_manager.dealer.ace_counts = 1
        # self.gamestate_manager.dealer.print_hand(second_card_visible=True)


        # deal dealer cards
        first_card =  self.gamestate_manager.dealer.cards[0]
        # create first card at correct position
        GUI_card = GUICard(first_card.color_string, first_card.image_value, self.CARD_SCALE)
        GUI_card.position = self.player_mats_list[0][0].position
        self.card_list.append(GUI_card)
        self.card_dict_data_access[first_card.unique_id] = GUI_card

        # create face down second card at correct position
        GUI_card = GUICard("Back_green", "5", self.CARD_SCALE)
        GUI_card.position = self.player_mats_list[0][1].position
        self.card_list.append(GUI_card)

        
        dealer_blackjack = self.gamestate_manager.evaluate_dealt_cards()

        # TODO: GUI HANDLE DEALER BLACKJACK INSTEAD OF EXITING GAME
        
        if dealer_blackjack:
            print("DEALER BLACKJACK")
            exit(10)

        
        # update name and money
        self.update_player_name_line()
        self.game_phase += 1

    def player_turn_phase(self):
        if self.active_player_index is None:
            self.active_player_index = 0
            self.game_phase += 1
            print("TURN ACTION PHASE FINISHED")
            return

        current_player = None
        # if a player splits --> creates split player --> then always handles split player first
        if self.split_player is None:
            current_player = self.player_list[self.active_player_index]
            if current_player not in self.gamestate_manager.current_playing_players:
                self.active_player_index += 1
                self.check_player_index()
                return
        
        else:
            current_player = self.split_player
            if current_player not in self.gamestate_manager.split_player_round_list:
                self.split_player = None
                return
        

        valid_player_turn_actions = self.gamestate_manager.get_valid_player_actions(current_player)

        if current_player.gui_player:
            if self.input_active == False:
                self.add_player_turn_action_field_widget()
            else:
                if self.gui_turn_action is None:
                    self.send_input = False
                    return
                
                if not self.send_input:
                    return

                if self.gui_turn_action not in valid_player_turn_actions: 
                    return

                split_player_active = False
                if self.split_player is current_player:
                    split_player_active = True

                turn_finished, self.split_player = self.gamestate_manager.player_turn(current_player, self.gui_turn_action)
                
                # UPDATE GUI CARDS / DRAW ALL CARDS OF PLAYER NEWLY
                player_mats = self.player_mats_list[self.active_player_index+1]
                if self.split_player is not None and not split_player_active:
                    self.split_player_mats_dict[self.active_player_index] = arcade.SpriteList()
                elif self.split_player is not None:
                    player_mats = self.split_player_mats_dict[self.active_player_index]
                reverse_offset = False if self.active_player_index < self.NUMBER_OF_HANDS_PER_SIDE else True
                draw_split_player = True if self.split_player is not None or current_player.split_this_round else False
                self.update_gui_player(current_player.cards, player_mats, reverse_offset, self.active_player_index, draw_split_player, split_player_active)

                if split_player_active:
                    if turn_finished:
                        self.split_player = None
                    else:
                        self.split_player = current_player
                elif turn_finished and self.split_player is None:
                    self.gui_turn_action = None
                    self.active_player_index += 1
                
                
                self.send_input = False
        else:
            if self.input_active:
                self.remove_widgets()
            else:
                turn_action = current_player.make_turn()
                if turn_action not in valid_player_turn_actions: 
                    return

                split_player_active = False
                if self.split_player is current_player:
                    split_player_active = True

                turn_finished, self.split_player = self.gamestate_manager.player_turn(current_player, turn_action)
                
                # UPDATE GUI CARDS
                player_mats = self.player_mats_list[self.active_player_index+1]
                if self.split_player is not None and not split_player_active:
                    self.split_player_mats_dict[self.active_player_index] = arcade.SpriteList()
                elif split_player_active:
                    player_mats = self.split_player_mats_dict[self.active_player_index]
                reverse_offset = False if self.active_player_index < self.NUMBER_OF_HANDS_PER_SIDE else True
                draw_split_player = True if self.split_player is not None or current_player.split_this_round else False
                self.update_gui_player(current_player.cards, player_mats, reverse_offset, self.active_player_index, draw_split_player, split_player_active)
    
                if split_player_active:
                    if turn_finished:
                        self.split_player = None
                    else:
                        self.split_player = current_player
                elif turn_finished and self.split_player is None:
                    self.active_player_index += 1
        self.check_player_index()


    def check_player_index(self):
        if self.active_player_index == len(self.player_list):
            self.active_player_index = None
            self.remove_widgets()

    def dealer_phase(self):
        # HANDLE DEALER TURN AND GUI
        self.gamestate_manager.dealer_turn()
        dealer_mats = self.player_mats_list[0]
        
        self.update_gui_player(self.gamestate_manager.dealer.cards, dealer_mats)
        self.game_phase += 1
    
    def update_player_name_line(self, index=None):
        # update all player name lines if no index given
        if index is None:
            for i in range(len(self.player_text_list)-1):
                self.player_text_list[i+1].text = "{} ({}): {}".format(self.player_list[i].name, self.player_list[i].money, self.player_list[i].current_bet)
        else:
          self.player_text_list[index+1].text = "{} ({}): {}".format(self.player_list[index].name, self.player_list[index].money, self.player_list[index].current_bet)  

    def update_gui_player(self, player_card_list, mats_list, reverse_offset = False, index=None, draw_split_player = False, split_player_active = False):
        self.update_player_name_line(index)

        scale = 1
        if draw_split_player:
            scale = 0.5


        x_offset = self.MAT_X_OFFSET
        if reverse_offset:
            x_offset = -self.MAT_X_OFFSET
        
        for i, card in enumerate(player_card_list):
            GUI_card = GUICard(card.color_string, card.image_value, self.CARD_SCALE * scale)
            key = card.unique_id

            # create new piles if needed
            if i >= len(mats_list):
                pile = arcade.SpriteSolidColor(int(self.MAT_WIDTH * scale), int(self.MAT_HEIGHT * scale), arcade.csscolor.DARK_OLIVE_GREEN)
                pile.position = mats_list[-1].position[0] + x_offset, mats_list[-1].position[1]
                    
                mats_list.append(pile) 
                self.pile_mat_list.append(pile)
            # remove old unscaled card
            elif key in self.card_dict_data_access:
                old_card = self.card_dict_data_access[key]
                if old_card in self.card_list:
                    self.card_list.remove(old_card)
                    self.card_dict_data_access.pop(key)
            
            # only scale width and height of existing mats once
            if self.split_player is not None and not split_player_active:
                mats_list[i].width *= scale
                mats_list[i].height *= scale
                
            GUI_card.position = mats_list[i].position
            self.card_list.append(GUI_card)
            self.card_dict_data_access[key] = GUI_card

        # draw initial cards of split player if split was action in this turn (and offset cards from original player)
        if self.split_player is not None and not split_player_active:
            split_mat_list = self.split_player_mats_dict[self.active_player_index]
            for i, card in enumerate(self.split_player.cards):
                pile = arcade.SpriteSolidColor(int(self.MAT_WIDTH * scale), int(self.MAT_HEIGHT * scale), arcade.csscolor.DARK_OLIVE_GREEN)
                if i == 0:
                    pile.position = mats_list[0].position[0], mats_list[0].position[1] - mats_list[i].height
                else:
                    pile.position = split_mat_list[-1].position[0] + x_offset, split_mat_list[-1].position[1]
                    
                    
                split_mat_list.append(pile) 
                self.pile_mat_list.append(pile)
                GUI_card = GUICard(card.color_string, card.image_value, self.CARD_SCALE * scale)
                GUI_card.position = pile.position
                self.card_list.append(GUI_card)
                key = card.unique_id
                self.card_dict_data_access[key] = GUI_card

    def evaluation_phase(self):
        # HANDLE EVALUATION AND GUI
        winning_player_list = self.gamestate_manager.evaluate_round() 
        results_string_list = []
        for i, (player, player_win) in enumerate(winning_player_list):
            print("\n{} Win: {}".format(player.name, player_win))
            results_string_list += ["\n"]
            results_string_list += ["{} Win: {}".format(player.name, player_win)]

        if len(results_string_list) == 0:
            results_string_list = ["Dealer wins\n No players left that did not go bust"]
        
        results_string_list += ["\n"]
        print("FINAL STRING: {}".format(results_string_list))
        self.add_results_widget(''.join(results_string_list))

        self.update_player_name_line()
        self.game_phase += 1

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.SPACE:
            # # TODO: make depending on currently playing player / valid check
            # pile = arcade.SpriteSolidColor(self.MAT_WIDTH, self.MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            # pile.position = self.player_mats_list[0][-1].position[0] + self.MAT_X_OFFSET, self.player_mats_list[0][-1].position[1]
            # self.pile_mat_list.append(pile)
            # self.player_mats_list[0].append(pile)
            # print("APPENDING NEW PILE")

            self.game_phase += 1

        if key == arcade.key.ENTER:
            if self.input_active:
                self.send_input = True
            

    def add_bet_input_field_widget(self):
        self.input_active = True
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def add_player_turn_action_field_widget(self):
        self.input_active = True
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.turn_option_box)
        )

        # BORDER RESULTS IN A BUG WHERE CHILD IS DRAWN MULTIPLE TIMES
        # border = arcade.gui.UIBorder(
        #     child=self.ui_input_box,
        #     border_width = 2,
        #     border_color= arcade.color.AFRICAN_VIOLET
        # )

        # self.ui_manager.add(border)

    def add_results_widget(self, text):
        self.input_active = True
        self.results_widget_box.children[-1].text = text
        self.results_widget_box.children[-1].fit_content()

        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.results_widget_box)
        )    

    def remove_widgets(self):
        self.ui_manager.clear()
        self.input_active = False


