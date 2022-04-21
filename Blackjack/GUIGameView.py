import math
import arcade
import arcade.gui
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton
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

        # list holding a list of cards for every player
        self.player_mats_list = None

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

    def setup(self, player_list):
        """ Set up the game variables. Call to re-start the game. """
        self.ui_manager.clear()
        self.ui_manager.enable()
        
        self.game_phase = 0
        self.active_player_index = 0

        if not player_list:
            raise RuntimeError("There were no players specified") 
        
        self.player_list = player_list
        self.player_text_list = []
        # prepare a list for every player (for convenient access and adding of mats)
        self.player_mats_list = [[] for _ in range(len(player_list)+1)]

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats that cards lay on
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create players start hands placeholder
        self.NUMBER_OF_HANDS_PER_SIDE = math.ceil(len(self.player_list) / 2)
        print("PLAYER COUNT: {}".format(len(self.player_list)))
        (self.CARD_SCALE, self.MAT_HEIGHT, self.MAT_WIDTH, self.MAT_X_OFFSET, MAT_Y_OFFSET, BOTTOM_Y, TOP_Y, START_X) = get_gui_constants(self.NUMBER_OF_HANDS_PER_SIDE, self.SCREEN_HEIGHT)
        print("NUMBER_OF_HANDS_PER_SIDE: {}".format(self.NUMBER_OF_HANDS_PER_SIDE))
        

        #  TODO: REMOVE / MOVE DOWN AGAIN
        self.card_list = arcade.SpriteList()

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

        for i in range(len(self.player_list)):

            # prepare for drawing player names
            if i > self.NUMBER_OF_HANDS_PER_SIDE-1:
                x_text_name_position =  x_start_position + 0.5 * self.MAT_WIDTH + self.MAT_X_OFFSET
                text_anchor_x = "right"
            self.player_text_list.append(arcade.Text(
                self.player_list[i].name,
                start_x = x_text_name_position,
                start_y = TOP_Y - row_index * MAT_Y_OFFSET + self.MAT_HEIGHT / 2,
                color = arcade.color.BLACK,
                font_size = self.DEFAULT_FONT_SIZE,
                anchor_x = text_anchor_x
                ))

            # prepare start hand mats (2) for every player
            for j in range(2):
                pile = arcade.SpriteSolidColor(self.MAT_WIDTH, self.MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
                pile.position = x_start_position + j * self.MAT_X_OFFSET, TOP_Y - row_index * MAT_Y_OFFSET
                self.pile_mat_list.append(pile)
                self.player_mats_list[i+1].append(pile)
            

            print("INDEX I: {}".format(i))
            print("X POS: {}, Y POS: {}".format(x_start_position, TOP_Y - row_index * MAT_Y_OFFSET))
            
            # handle different positioning depending on index of player
            if i >= self.NUMBER_OF_HANDS_PER_SIDE-1:
                x_start_position = self.SCREEN_WIDTH - START_X - self.MAT_X_OFFSET
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
        card = GUICard("Back_green", "5", self.CARD_SCALE)
        card.position = START_X, TOP_Y + 2*VERTICAL_MARGIN_PERCENT * self.MAT_HEIGHT + self.MAT_HEIGHT
        self.card_list.append(card)


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
        # --- Method 2 for handling click events,
        # assign self.on_click_start as callback
        submit_button.on_click = self.on_click_submit
        
        self.ui_input_box = arcade.gui.UIInputText(
             width=self.DEFAULT_FONT_SIZE * 10,
             height=self.DEFAULT_FONT_SIZE,
             text="Set bet"
         )

        self.ui_input_box.cursor_index = len(self.ui_input_box.text)
        self.v_box = UIBoxLayout(
            children=[label, self.ui_input_box, submit_button]
        )

       


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
                    self.player_text_list[self.active_player_index+1].text += ": {}".format(bet)
                    if self.active_player_index+1 > self.NUMBER_OF_HANDS_PER_SIDE-1:
                        x_offset_gui_player = -(len(str(bet)) + 2)
                        self.player_text_list[self.active_player_index+1].x += x_offset_gui_player
                    
                    self.active_player_index += 1
                
                self.send_input = False
        else:
            if self.input_active:
                self.remove_bet_input_field_widget()
            else:
                bet = current_player.get_bet()
                if self.check_bet_input_valid(bet, current_player):
                    self.player_text_list[self.active_player_index+1].text += ": {}".format(bet)
                    if self.active_player_index+1 > self.NUMBER_OF_HANDS_PER_SIDE-1:
                        x_offset_gui_player = -(len(str(bet)) + 2)
                        self.player_text_list[self.active_player_index+1].x += x_offset_gui_player
                    
                    self.active_player_index += 1

        if self.active_player_index == len(self.player_list):
            self.active_player_index = None
            self.remove_bet_input_field_widget()

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

        # start from index 1 to handle dealer seperately
        for i in range(1, len(self.player_list)+1):
            cards =  self.player_list[i-1].cards
            # create first card at correct position
            GUI_card = GUICard(cards[0].color_string, cards[0].image_value, self.CARD_SCALE)
            GUI_card.position = self.player_mats_list[i][0].position
            self.card_list.append(GUI_card)
            # create second card at correct position
            GUI_card = GUICard(cards[1].color_string, cards[1].image_value, self.CARD_SCALE)
            GUI_card.position = self.player_mats_list[i][1].position
            self.card_list.append(GUI_card)
        
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
        # create face down second card at correct position
        GUI_card = GUICard("Back_green", "5", self.CARD_SCALE)
        GUI_card.position = self.player_mats_list[0][1].position
        self.card_list.append(GUI_card)

        
        dealer_blackjack = self.gamestate_manager.evaluate_dealt_cards()
        # TODO: GUI HANDLE DEALER BLACKJACK INSTEAD OF EXITING GAME
        
        if dealer_blackjack:
            print("DEALER BLACKJACK")
            exit(10)

        self.game_phase += 1

    def player_turn_phase(self):
        # TODO: HANDLE PLAYER TURN AND GUI
        pass

    def dealer_phase(self):
        # TODO: HANDLE DEALER TURN AND GUI
        self.gamestate_manager.dealer_turn()

    def evaluation_phase(self):
        # TODO: HANDLE EVALUATION AND GUI
        self.gamestate_manager.evaluate_round()  

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
            

    def on_click_submit(self, event):
        self.send_input = True

    def add_bet_input_field_widget(self):
        self.input_active = True
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        # BORDER RESULTS IN A BUG WHERE CHILD IS DRAWN MULTIPLE TIMES
        # border = arcade.gui.UIBorder(
        #     child=self.ui_input_box,
        #     border_width = 2,
        #     border_color= arcade.color.AFRICAN_VIOLET
        # )

        # self.ui_manager.add(border)



    def remove_bet_input_field_widget(self):
        self.ui_manager.clear()
        self.input_active = False


