# Constants for sizing
MAX_CARD_SCALE = 0.3

# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.25

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.05
HORIZONTAL_MARGIN_PERCENT = 0.05

Y_MARGIN = 0.05
# NUMBER_OF_HANDS_PER_SIDE = int(TOP_Y / MAT_Y_OFFSET)

def calculate_gui_constants(CARD_SCALE, SCREEN_HEIGHT):
    # How big are the cards?
    CARD_WIDTH = 140 * CARD_SCALE
    CARD_HEIGHT = 190 * CARD_SCALE
    MAT_HEIGHT = MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
    MAT_WIDTH = MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

    # The Y of the bottom row (2 piles)
    BOTTOM_Y = BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

    # The X of where to start putting things on the left side
    MAT_X_OFFSET = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT * 2
    START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

    # Fixed positions and offsets
    NAME_HEIGHT = SCREEN_HEIGHT / 30
    MAT_Y_OFFSET = MAT_HEIGHT + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT * 2 + NAME_HEIGHT
    TOP_Y = SCREEN_HEIGHT - SCREEN_HEIGHT * Y_MARGIN - MAT_Y_OFFSET

    return CARD_SCALE, MAT_HEIGHT, MAT_WIDTH, MAT_X_OFFSET, MAT_Y_OFFSET, BOTTOM_Y, TOP_Y, START_X

def get_gui_constants(NUMBER_OF_HANDS_PER_SIDE, SCREEN_HEIGHT):
    # add for dealer space
    NUMBER_OF_HANDS_PER_SIDE += 1

    Y_SPACE = SCREEN_HEIGHT - SCREEN_HEIGHT * 2 * Y_MARGIN 
    # find maximum possible card scale
    # 0.9 because of space needed for name
    calc_card_scale = int((Y_SPACE / NUMBER_OF_HANDS_PER_SIDE) - SCREEN_HEIGHT/20) / MAT_PERCENT_OVERSIZE / 190
    print("SCALE BEFORE: {}".format(calc_card_scale))
    if calc_card_scale > MAX_CARD_SCALE:
        calc_card_scale = MAX_CARD_SCALE
    
    print("SCALE AFTER: {}".format(calc_card_scale))
    return calculate_gui_constants(calc_card_scale, SCREEN_HEIGHT)


# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]