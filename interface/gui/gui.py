import tkinter as tk
from tkinter import simpledialog, messagebox
import webbrowser


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


def display_message(message):
    print(message)


def turn_choice():
    choice = 0
    display_message('Select an option:')

    while choice < 1 or choice > 2:
        print("1. Make a move\n2. Swap a card")
        choice = int(input("Choose (enter a number) (1 or 2): "))

    return choice


def get_move_input():
    x = int(input("X: "))
    y = int(input("Y: "))

    return x, y


def add_line_break():
    print("========== ********** ==========")


def display_valid_move(player_name, chosen_move, board):
    card_string = board.get_card_string(chosen_move[0], chosen_move[1])
    display_message('Valid Move!')
    display_message('{} chose to move to card {} at position {}'.format(player_name, card_string, chosen_move))


def display_valid_swap(player_name, joker_position, card_position, board):
    card_string = board.get_card_string(card_position[0], card_position[1])
    display_message('Valid Swap!')
    display_message('{} chose to swap a [ Joker ] at position {} with card {} at position {}'.format(player_name,
                                                                                                 joker_position,
                                                                                                 card_string,
                                                                                                 card_position))


def center_window(window, width, height):
    # Get the screen dimension
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Find the center point
    center_x = int(screen_width/2 - width/2)
    center_y = int(screen_height/2 - height/2)

    # Set the position of the window to the center of the screen
    window.geometry(f'{width}x{height}+{center_x}+{center_y}')


def show_game_rules():
    rules_screen = tk.Toplevel()
    rules_screen.title("Game Rules")

    center_window(rules_screen, 900, 900)  # Width = 400, Height = 300

    rules_text = "Here are the game rules:\n\n"  # Add your game rules text here
    tk.Label(rules_screen, text=rules_text, justify=tk.LEFT, padx=10).pack(side="top", fill="both", expand=True)

    # Link
    link = "https://www.example.com"  # Replace with your actual link
    link_label = tk.Label(rules_screen, text="Click here for more info", fg="blue", cursor="hand2")
    link_label.pack()
    link_label.bind("<Button-1>", lambda e: webbrowser.open_new(link))


def ask_player_name(title, parent):
    while True:
        name = simpledialog.askstring("Player Name", f"Enter {title}'s name:", parent=parent)
        if name:
            return name
        messagebox.showwarning("Name Required", "Please enter a name to continue.")
