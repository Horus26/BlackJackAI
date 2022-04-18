import math
from turtle import position
import arcade
from .GUIConstants import get_gui_constants, VERTICAL_MARGIN_PERCENT, CARD_SUITS, CARD_VALUES
from .GUICard import GUICard



class GUIGame(arcade.Window):

    def __init__(self, width = 800, height = 600, title = "Blackjack"):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

        # Sprite list for cards
        self.card_list = None

        # Sprite list for places where cards can be placed (mats)
        self.pile_mat_list = None

        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.TITLE = title

    def setup(self, player_list):
        """ Set up the game variables. Call to re-start the game. """
        if not player_list:
            raise RuntimeError("There were no players specified") 
        
        self.player_list = player_list
        self.player_text_list = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create players start hands placeholder
        row_index = 0
        NUMBER_OF_HANDS_PER_SIDE = math.ceil(len(self.player_list) / 2)
        print("PLAYER COUNT: {}".format(len(self.player_list)))
        (CARD_SCALE, MAT_HEIGHT, MAT_WIDTH, MAT_X_OFFSET, MAT_Y_OFFSET, BOTTOM_Y, TOP_Y, START_X) = get_gui_constants(NUMBER_OF_HANDS_PER_SIDE, self.SCREEN_HEIGHT)
        print("NUMBER_OF_HANDS_PER_SIDE: {}".format(NUMBER_OF_HANDS_PER_SIDE))
        x_start_position = START_X

        #  TODO: REMOVE / MOVE DOWN AGAIN
        self.card_list = arcade.SpriteList()


        DEFAULT_LINE_HEIGHT = 45
        DEFAULT_FONT_SIZE = 60 * CARD_SCALE
        x_text_name_position = x_start_position - MAT_WIDTH / 2
        text_anchor_x = "left"
        for i in range(len(self.player_list)):
            if i > NUMBER_OF_HANDS_PER_SIDE-1:
                x_text_name_position =  x_start_position + 0.5 * MAT_WIDTH + MAT_X_OFFSET
                text_anchor_x = "right"

            # prepare for drawing player names
            self.player_text_list.append(arcade.Text(
                self.player_list[i].name,
                x_text_name_position,
                TOP_Y - row_index * MAT_Y_OFFSET + MAT_HEIGHT / 2,
                arcade.color.BLACK,
                DEFAULT_FONT_SIZE,
                anchor_x = text_anchor_x
                ))

            for j in range(2):
                pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
                pile.position = x_start_position + j * MAT_X_OFFSET, TOP_Y - row_index * MAT_Y_OFFSET
                self.pile_mat_list.append(pile)
                
                # TODO: REMOVE DEBUG
                card = GUICard("Clubs", CARD_VALUES[i], CARD_SCALE)
                card.position = x_start_position + j * MAT_X_OFFSET, TOP_Y - row_index * MAT_Y_OFFSET
                self.card_list.append(card)

            print("INDEX I: {}".format(i))
            print("X POS: {}, Y POS: {}".format(x_start_position, TOP_Y - row_index * MAT_Y_OFFSET))
            if i >= NUMBER_OF_HANDS_PER_SIDE-1:
                x_start_position = self.SCREEN_WIDTH - START_X - MAT_X_OFFSET
                if i >= NUMBER_OF_HANDS_PER_SIDE:
                    row_index -= 1
            else:
                row_index += 1

        # prepare for drawing dealer name
        self.player_text_list.append(arcade.Text(
            "Dealer",
            self.SCREEN_WIDTH/2 - MAT_WIDTH / 2,
            TOP_Y + 2*VERTICAL_MARGIN_PERCENT * MAT_HEIGHT + MAT_HEIGHT * 1.5,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE,
            anchor_x = "center"
            ))

        # create dealer start hand placeholder
        for j in range(2):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = self.SCREEN_WIDTH/2 - MAT_X_OFFSET + j * MAT_X_OFFSET, TOP_Y + 2*VERTICAL_MARGIN_PERCENT * MAT_HEIGHT + MAT_HEIGHT
            self.pile_mat_list.append(pile)

        # Sprite list with all the cards
        # self.card_list = arcade.SpriteList()

        # Create every card
        for card_suit in CARD_SUITS:
            counter = 0
            for card_value in CARD_VALUES:
                card = GUICard(card_suit, card_value, CARD_SCALE)
                card.position = START_X + counter * MAT_X_OFFSET, TOP_Y + 2*VERTICAL_MARGIN_PERCENT * MAT_HEIGHT + MAT_HEIGHT
                self.card_list.append(card)
                # counter += 1
        card = GUICard("Back_green", "5", CARD_SCALE)
        card.position = START_X, TOP_Y + 2*VERTICAL_MARGIN_PERCENT * MAT_HEIGHT + MAT_HEIGHT
        self.card_list.append(card)


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

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def start_gui(self):
        arcade.run()

