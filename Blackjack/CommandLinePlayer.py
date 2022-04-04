from .Player import Player
from .Constants import PLAYER_ACTIONS

class CommandLinePlayer(Player) :
    def __init__(self, player_name, start_money):
        super(). __init__(player_name, start_money)

    def make_turn(self):
        turn_action = self.handle_input(isAction = True)
        return turn_action

    def determine_bet(self):
        bet = self.handle_input(isAction = False)
        print("User player {} determining bet: {}".format(self.name, bet))
        return bet

    def handle_input(self, isAction = False):
        if isAction: return self.handle_action_input()
        else: return self.handle_bet_input()

    def handle_bet_input(self):
        print("Waiting for user input: enter a valid number (floating point allowed in format x.xx)")
        keyboard_input = None
        while keyboard_input is None:
            try:
                keyboard_input = float(input("Bet: "))
                if keyboard_input > self.money:
                    print("Invalid Input. You do not have this much money.")
                    keyboard_input = None
            except ValueError:
                print ("Error: '{}' is not a valid float!".format(keyboard_input))
        return keyboard_input

        

    def handle_action_input(self):
        self.print_hand()
        print("Waiting for user input: h=hit, s=stand, p=split, d=double")
        keyboard_input = None
        while(keyboard_input is None):
            keyboard_input = input("Action: ")
            if keyboard_input == "h":
                keyboard_input = PLAYER_ACTIONS["Hit"]
            elif keyboard_input == "s":
                keyboard_input = PLAYER_ACTIONS["Stand"]
            elif keyboard_input == "p":
                keyboard_input = PLAYER_ACTIONS["Split"]
            elif keyboard_input == "d":
                keyboard_input = PLAYER_ACTIONS["Double"]
            else:
                print("Invalid Input. Try again")
                keyboard_input = None

        return keyboard_input
        
