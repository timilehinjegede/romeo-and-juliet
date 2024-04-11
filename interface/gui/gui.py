import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.font import Font
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

    # Set window background color
    rules_screen.configure(bg='#00A550')

    center_window(rules_screen, 900, 900)  # Width = 400, Height = 300

    # Display the rules in a scrollable text widget
    text_widget = tk.Text(rules_screen, wrap="word", bg='#00A550', fg='white', font=Font(size=12))
    text_widget.pack(padx=10, pady=10, fill="both", expand=True)

    # Define a tag for bold text
    bold_font = ('Arial', 14, 'bold')
    text_widget.tag_configure('bold', font=bold_font)
    text_widget.tag_configure('extra-bold', font=('Arial', 18, 'bold'))

    # Game rules text
    rules_parts = [
        ("ROMEO (Or Abélard & Héloïse, Sid & Doris, etc)\n\n", 'extra-bold'),
        ("Players: 2\nCards: 52\nType: Positional\n\n", None),
        ("Adapted from an unpublished game called Card Maze by Eric Solomon.\n\n", None),
        ("Start:\n", 'bold'),
        ("From a 52-card pack remove the Queen of clubs, the Queen of diamonds and one of the Sevens. "
         "Deal the remaining 49 cards face up in seven rows of seven. Turn the three Sevens face down "
         "and call them Jokers. (Or, if you prefer, use real Jokers face up instead of Sevens face down.) "
         "Then exchange the spade Queen for the bottom left corner card, and the heart Queen for the top right "
         "corner card, so that the two Queens occupy diagonally opposite corners.\n"
         "One player is Black, and places a black chess king on the heart Queen. The other player is Red and "
         "correspondingly places a nominally red (or actually white) chess king on the spade Queen. Each chess "
         "king is a Romeo and each card Queen a Juliet.\n\n", None),
        ("Object:\n", 'bold'),
        ("To be the first to move your Romeo to your corresponding Juliet at the diagonally opposite corner.\n\n", None),
        ("Play:\n", 'bold'),
        ("Red moves first and each plays in turn. At each turn you either move your Romeo or swap two cards in "
         "the layout, in accordance with the rules below.\n\n", None),
        ("Moving your Romeo:\n", 'bold'),
        ("The rules of movement are: From a red numeral you move vertically, up or down as preferred, the number "
         "of cards indicated by the numeral you are on (counting ace as one and others at face value); From a black "
         "numeral you move horizontally, left or right as preferred, the number of cards indicated by the card you "
         "are on. If your move takes you beyond the edge of the board you pass immediately to the first card at the "
         "opposite end of the same row or column and continue in the same direction. You may not land on or jump "
         "over your opponent's Romeo, nor may you land again on the Queen you started from. From a King, you move "
         "like a chess king, one step to any one of up to eight immediately surrounding cards, except that you may "
         "not make a move that would take you over an edge. From a Jack, you move like a chess knight to any one of "
         "up to eight cards, except that you may not make a move that would take you over an edge. From a Joker you "
         "move to any card from which you could legally have reached it. (Including the one you last moved from.)\n\n", None),
        ("Swapping two cards:\n", 'bold'),
        ("On your turn to play, you may swap one of the Jokers for any other card in the same row or column. Neither "
         "of these cards may be occupied, neither may be one of the cards involved in the most recently performed swap, "
         "and neither may be a Queen.\n\n", None),
        ("Winning:\n", 'bold'),
        ("To win, you must reach your Juliet on an exact number of moves. That is, if moving from a numeral card you "
         "must take the full value of your move. You may, of course, reach her from a King or a Jack if possible.\n\n", None),
        ("Notes:\n", 'bold'),
        ("Note 1. Counting 'over the edge' is easy if you remember that moving seven cards in a given direction would "
         "bring you right back to the one you started from (which is why Sevens are omitted). Therefore, moving 8, 9 or "
         "10 is the same as moving (respectively) 1, 2 or 3 in the same direction. Similarly, moving 4, 5 or 6 in one "
         "direction is the same as moving (respectively) 3, 2 or 1 in the opposite direction.\n"
         "Note 2. But you can, of course, get to a card on the other side of the other Romeo by moving away from it in "
         "the opposite direction and continuing from 'over the edge'.", None)
    ]

    # Insert each part of the rules with appropriate tagging
    for text, tag in rules_parts:
        text_widget.insert('end', text, tag)

    text_widget.config(state="disabled") 
    # Link
    link = "https://www.parlettgames.uk/oricards/romeo.html"  # Replace with your actual link
    link_label = tk.Label(rules_screen, text="CLICK HERE FOR MORE INFO", fg="blue", cursor="hand2")
    link_label.pack(pady=10)
    link_label.bind("<Button-1>", lambda e: webbrowser.open_new(link))


def ask_player_name(title, parent):
    while True:
        name = simpledialog.askstring("Player Name", f"Enter {title}'s name:", parent=parent)
        if name:
            return name
        messagebox.showwarning("Name Required", "Please enter a name to continue.")
