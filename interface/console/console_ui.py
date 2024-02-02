def game_welcome():
    print("Welcome to the Romeo and Juliet Game!")
    add_line_break()


def welcome_players(player1, player2):
    print(f"Welcome {player1} and {player2}!!!")
    add_line_break()


def ask_for_player_name(player_number):
    return input(f"Enter Player {player_number}'s name: ")


def display_welcome_message(player1_name, player2_name):
    print(f"Welcome {player1_name} and {player2_name}!")
    add_line_break()


def display_setup_message(message):
    print(message)


def add_line_break():
    print("===== ***** =====")
