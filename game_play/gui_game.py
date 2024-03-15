import tkinter as tk

from tkinter.font import Font
from core.classes.game_setup.player import Player
from core.classes.moves import moves
from core.classes.moves.black_numeral_move import suggest_black_numeral_moves
from core.classes.moves.joker_move import suggest_joker_positions, get_possible_moves_to_joker
from core.classes.moves.king_move import suggest_king_moves
from core.classes.moves.knight_move import suggest_knight_moves
from core.classes.moves.red_numeral_move import suggest_red_numeral_moves
from core.classes.moves.swap import Swap
from interface.console import console_ui
from interface.gui import gui
from PIL import Image, ImageTk

class GUIGame:
    def __init__(self, board):
        self.board = board
        self.player1_turn = True
        self.game_over = False
        self.valid_move = False
        self.is_joker = False
        self.turn = 1
        self.is_first_move = True
        self.card_labels = [[None for _ in range(7)] for _ in range(7)]  # 7x7 grid for labels

        # players
        self.player1 = None
        self.player2 = None

        # game screen
        self.game_screen = tk.Tk()
        # hide the root window
        self.game_screen.withdraw()

        self.passed_welcome = False

        self.black_king = Image.open('resources/romeos/black_king.png').convert('RGBA')
        self.red_king = Image.open('resources/romeos/red_king.png').convert('RGBA')

        self.highlighted_positions = []
        self.chosen_move = None

        self.is_valid_move = tk.StringVar()

        self.turn_labels = {}  # Dictionary to store turn labels for each player
    
    def request_players_info(self):

        intro_window = tk.Toplevel()
        intro_window.title("Romeo and Juliet Game")

        gui.center_window(intro_window, 900, 900)

        play_with_human_button = tk.Button(intro_window, text="Play with Human",
                                           command=lambda: self.play_with_human(intro_window))
        play_with_ai_button = tk.Button(intro_window, text="Play with AI", command=self.play_with_ai)
        game_rules_button = tk.Button(intro_window, text="Game Rules", command=gui.show_game_rules)

        play_with_human_button.pack()
        play_with_ai_button.pack()
        game_rules_button.pack()

        intro_window.mainloop()

        self.player1_move_button
        self.player1_swap_button
        self.player2_move_button
        self.player2_swap_button

        # ask for the players to enter their names
        # player1_name = console_ui.ask_for_player_name(1)
        # player1_name = "Carl (Player 1)"
        # player2_name = console_ui.ask_for_player_name(2)
        # player2_name = "Jake (Player 2)"

        # create the players
        # self.player1 = Player(player1_name, 1)
        # self.player2 = Player(player2_name, 2)

        # welcome the players
        # gui.welcome_players(player1_name, player2_name)

        # gui.display_message("{} is nominated as RED (white) and {} is nominated as BLACK".format(player1_name,
        #                                                                                                 player2_name))
        # display the initial board
        # player1 = self.player1
        # player2 = self.player2
        # self.board.display_board(player1.xPosition, player1.yPosition, player2.xPosition, player2.yPosition)

    def update_button_visibility(self):
                # Update button visibility based on current player and whether it's an initial move
        if self.is_first_move:
            # If it's an initial move, hide buttons for both players
            if hasattr(self, 'player1_move_button'):
                self.player1_move_button.pack_forget()
                self.player1_swap_button.pack_forget()
            if hasattr(self, 'player2_move_button'):
                self.player2_move_button.pack_forget()
                self.player2_swap_button.pack_forget()
            return
        # Hide buttons for player 1 and show for player 2, or vice versa
        if self.player1_turn:
            if hasattr(self, 'player1_move_button'):
                self.player1_move_button.pack(padx=5, pady=10)
                self.player1_swap_button.pack(padx=5, pady=10)
            if hasattr(self, 'player2_move_button'):
                self.player2_move_button.pack_forget()
                self.player2_swap_button.pack_forget()
        else:
            if hasattr(self, 'player2_move_button'):
                self.player2_move_button.pack(padx=5, pady=10)
                self.player2_swap_button.pack(padx=5, pady=10)
            if hasattr(self, 'player1_move_button'):
                self.player1_move_button.pack_forget()
                self.player1_swap_button.pack_forget()

    # Define the player sections
    def create_player_section(self, parent, player_name, nomination, player_number):
        frame = tk.Frame(parent)
    
        # Define a larger font
        large_font = Font(size=12)  # Adjust the size as needed

        # Player number label
        name_label = tk.Label(frame, text='Player {}'.format(player_number), anchor='center', padx=10, pady=10)
        name_label['font'] = large_font
        name_label.pack(fill='both', pady=15)

        # Player name label 
        name_label = tk.Label(frame, text='Player Name: ', anchor='center', padx=10)
        name_label['font'] = Font(size = 10)
        name_label.pack(fill='both')
        name_label = tk.Label(frame, text=player_name, anchor='center', padx=10, pady=10)
        name_label['font'] = large_font
        name_label.pack(fill='both')

        # Nomination label
        nomination_label = tk.Label(frame, text=nomination, anchor='center', padx=10, pady=10)
        nomination_label['font'] = large_font
        nomination_label.pack(fill='both')

        # "Your turn" label (shown conditionally, adjust this as per your logic)
        # turn_label = tk.Label(frame, text="Your turn", anchor='center', padx=10, pady=10)
        # turn_label['font'] = large_font
        turn_label = tk.Label(frame, text="", anchor='center', padx=0, pady=0, fg='red', width=20, wraplength=150)
        turn_label['font'] = Font(size=8)
        turn_label.pack(fill='both')
        self.turn_labels[player_number] = turn_label 

        # Buttons with color
        # Button to make a move
        move_button = tk.Button(frame, text="Make a Move", bg='green', fg='white', font=large_font,
                                command=lambda: self.move_card())

        # Button to swap a card
        swap_button = tk.Button(frame, text="Swap a Card", bg='blue', fg='white', font=large_font,
                                command=lambda: self.swap_card())

        # Store references to the buttons
        if player_number == 1:
            self.player1_move_button = move_button
            self.player1_swap_button = swap_button
        else:
            self.player2_move_button = move_button
            self.player2_swap_button = swap_button

        # "Your turn" label (shown conditionally, adjust this as per your logic)
        # if player_1_turn:
        # turn_label.pack(fill='both')

        return frame
    
    def display_label(self):
        self.turn_labels[1].config(font=Font(size=12, weight='bold'))
        self.turn_labels[2].config(font=Font(size=12, weight='bold'))
        # is_player_1 = player.player_number == 1
        p = self.player1 if self.player1_turn else self.player2
        if self.is_first_move:
            self.turn_labels[1].config(text="{}'s Turn for the initial move".format(p.name))
            self.turn_labels[2].config(text="{}'s Turn for the initial move".format(p.name))
        else:
            self.turn_labels[1].config(text="{}'s Turn to make a move or swap a card".format(p.name))
            self.turn_labels[2].config(text="{}'s Turn to make a move or swap a card".format(p.name))

        self.turn_labels[1].pack(fill='both')
        self.turn_labels[2].pack(fill='both')

    def update_card_grid(self):
        print("Updating the card grid => hightlighted positions:", self.highlighted_positions)
        card_width, card_height = 80, 120  # Set the dimensions for the card images

        for i in range(7):
            for j in range(7):
                            # Reset the label configurations and unbind previous events
                self.card_labels[i][j].config(image='', highlightthickness=0, highlightbackground=None)
                self.card_labels[i][j].unbind("<Button-1>")

                if (i, j) == (0, 6):  # Top left position for red queen
                    card_image_path = 'resources/card_images/queen_of_hearts.png'
                elif (i, j) == (6, 0):  # Bottom left position for black queen
                    card_image_path = 'resources/card_images/queen_of_spades.png'
                else:
                    card_image_path = self.board.get_card_image(i + 1, j + 1)  # Assuming 1-indexed positions

                if card_image_path and card_image_path != "No card at this position":
                    img = Image.open(card_image_path)
                    img = img.resize((card_width, card_height), Image.BOX)

                    if (i + 1, j + 1) == (self.player1.xPosition, self.player1.yPosition):
                        king_img = self.black_king
                        king_width, king_height = king_img.size
                        x = (card_width - king_width) // 2
                        y = (card_height - king_height) // 2
                        img.paste(king_img, (x, y), king_img)
                    elif (i + 1, j + 1) == (self.player2.xPosition, self.player2.yPosition):
                        king_img = self.red_king
                        king_width, king_height = king_img.size
                        x = (card_width - king_width) // 2
                        y = (card_height - king_height) // 2
                        img.paste(king_img, (x, y), king_img)

                    card_image = ImageTk.PhotoImage(img)
                else:
                    card_image = None

                if card_image:  # Only configure the label if there's an image
                    self.card_labels[i][j].config(image=card_image)
                    self.card_labels[i][j].image = card_image  # Keep a reference
                else:
                    self.card_labels[i][j].config(image='')  # Clear the image for empty cells

                position = (i + 1, j + 1)
                if position in self.highlighted_positions:
                    king_img = self.black_king if (i + 1, j + 1) == (self.player1.xPosition, self.player1.yPosition) else self.red_king
                    color = 'red' if self.player1_turn else 'black'
                    self.card_labels[i][j].config(highlightthickness=3, highlightbackground=color)
                    self.card_labels[i][j].bind("<Button-1>", lambda e, x=i, y=j: self.on_card_click(x, y, True))
                else:
                    self.card_labels[i][j].bind("<Button-1>", lambda e, x=i, y=j: self.on_card_click(x, y, False))

                self.card_labels[i][j].grid(row=i, column=j, sticky='nswe', padx=5, pady=5)

    def show_game_layout(self):
        root = self.game_screen

        # Section 1 - Player 1
        player1_frame = self.create_player_section(root, self.player1.name, "RED PLAYER", 1)
        player1_frame.grid(row=0, column=0, sticky='nswe')

        # Section 3 - Player 2
        player2_frame = self.create_player_section(root, self.player2.name, "BLACK PLAYER", 2)
        player2_frame.grid(row=0, column=8, sticky='nswe')

        # Section 2 - Card Grid (7x7)
        # Section 2 - Card Grid (7x7)
        # Initialize a 7x7 grid of Labels to hold card images
        card_frame = tk.Frame(root)
        card_frame.grid(row=0, column=1, columnspan=7, sticky='nswe')

        card_width = root.winfo_width() // 9  # Assuming there are 9 columns in the grid
        card_height = root.winfo_height() // 8  # Assuming there are 8 rows in the grid

        # Initialize a 7x7 grid of Labels to hold card images
        self.card_labels = [[tk.Label(card_frame) for _ in range(7)] for _ in range(7)]
        for i in range(7):
            for j in range(7):
                if (i, j) == (0, 6):  # Top left position for red queen
                    card_image_path = 'resources/card_images/queen_of_hearts.png'
                elif (i, j) == (6, 0):  # Bottom left position for black queen
                    card_image_path = 'resources/card_images/queen_of_spades.png'
                else:
                # Get the image for the card at the current position
                    card_image_path = self.board.get_card_image(i + 1, j + 1)  # Assuming 1-indexed positions

                if card_image_path and card_image_path != "No card at this position":
                    # Open the image file
                    img = Image.open(card_image_path)
                    # Resize the image
                    img = img.resize((80, 120), Image.BOX)

                    if (i + 1, j + 1) in [(self.player1.xPosition, self.player1.yPosition), (self.player2.xPosition, self.player2.yPosition)]:
                        king_img = self.black_king if (i + 1, j + 1) == (self.player1.xPosition, self.player1.yPosition) else self.red_king
                        king_width, king_height = king_img.size
                        x = (80 - king_width) // 2
                        y = (120 - king_height) // 2
                        img.paste(king_img, (x, y), king_img)

                    # overlay the king images based on player positions
                    # if (i, j) == (self.player1.xPosition - 1, self.player1.yPosition - 1):
                    #     img.paste(self.black_king, (10, 10), self.black_king)
                    # elif (i, j) == (self.player2.xPosition - 1, self.player2.yPosition - 1):
                    #     img.paste(self.red_king, (10, 10), self.red_king)

                    card_image = ImageTk.PhotoImage(img)
                else:
                    # You might want to have a default image for empty spaces or a placeholder
                    card_image = None  # Placeholder for an empty image

                if card_image:  # Only configure the label if there's an image
                    self.card_labels[i][j].config(image=card_image)
                    self.card_labels[i][j].image = card_image  # Keep a reference
                self.card_labels[i][j].grid(row=i, column=j, sticky='nswe', padx=5, pady=5)

                position = (i + 1, j + 1)
                color = 'red' if self.player1_turn else 'black'
                if position in self.highlighted_positions:
                    self.card_labels[i][j].config(highlightthickness=3, highlightbackground=color)
                    self.card_labels[i][j].bind("<Button-1>", lambda e, x=i, y=j: self.on_card_click(x, y, True))
                else:
                    self.card_labels[i][j].bind("<Button-1>", lambda e, x=i, y=j: self.on_card_click(x, y, False))

        # Configure the grid weight
        root.grid_rowconfigure(0, weight=1)

        for i in range(7):
            root.grid_columnconfigure(i + 1, weight=1)
            card_frame.grid_rowconfigure(i, weight=1)
            card_frame.grid_columnconfigure(i, weight=1)

        # Player sections weight configuration
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(8, weight=1)

    def move_card(self):
        current_player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        self.handle_move_card(current_player, opponent)
        self.display_label()

    def swap_card(self):
        current_player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        self.handle_swap_card(current_player, opponent)
        self.display_label()

    def on_card_click(self, x, y, is_valid):
        if is_valid:
            print(f"Clicked on a valid card at position ({x}, {y})")
            # Perform necessary actions for a valid move
            # Update player positions, etc.
            # self.valid_move = (x, y)
            self.is_valid_move.set(f"{x}, {y}")
        else:
            print(f"Clicked on an invalid card at position ({x}, {y})")
            # Handle invalid move (show message, etc.)
            gui.messagebox.showinfo("Invalid Move", "The card selected cannot be moved to!")

    def handle_player_move(self, player, opponent):

        if self.is_first_move:
            self.handle_initial_move(player, opponent)

        else:
            # console_ui.display_message("\n<Move {}>".format(self.turn))
            # COME choice = console_ui.turn_choice()

            # if choice == 1:
            self.handle_move_card(player, opponent)
            # elif choice == 2:
                # self.handle_swap_card(player, opponent)
            
    def display_current_card(self, player):
        card_face = self.board.get_card_string(player.xPosition, player.yPosition)
        console_ui.add_line_break()
        console_ui.display_message("{} is currently on: {}".format(player.name, card_face))
    
    def make_move(self, player_number):
        print(f"Player {player_number} is making a move.")
        # Implement the logic for making a move
        # This could involve updating the game state, player positions, etc.

    def swap_card(self, player_number):
        print(f"Player {player_number} is swapping a card.")
        # Implement the logic for swapping a card
        # This could involve changing a card in the player's hand, etc.

    def handle_move_card(self, player, opponent):
        # self.update_button_visibility(player.player_number)
        valid_move = False

        while not valid_move:
            card = self.board.get_card_string(player.xPosition, player.yPosition)

            # joker move
            if "JOKER" in card:
                valid_move = self.handle_joker_move(player, opponent)
            # king move
            elif "K" in card:
                valid_move = self.handle_king_move(player, opponent)
            # Jack move
            elif "J" in card:
                valid_move = self.handle_knight_move(player, opponent)
            # black numeral card => SPADES OR CLUBS
            elif "\u2660" in card or "\u2663" in card:
                valid_move = self.handle_black_numeral_move(player, opponent)
            elif "\u2661" in card or "\u2662" in card:
                valid_move = self.handle_red_numeral_move(player, opponent)


        self.on_make_move(player.player_number)

    def select_move(self, suggested_moves, player):
        self.highlighted_positions = suggested_moves

        self.update_card_grid()

        # chosen_move = moves.choose_move_from_suggestions(king_move_suggestions, self.board)
        self.game_screen.wait_variable(self.is_valid_move)

        x, y = map(int, self.is_valid_move.get().split(", "))


        self.valid_move = True

        self.highlighted_positions.clear()

        if player.player_number == 1:
            self.player1.set_position(x + 1, y + 1)
        else:
            self.player2.set_position(x + 1, y + 1)


        self.update_card_grid()

    def handle_initial_move(self, player, opponent):
        self.valid_move = False

        while not self.valid_move:
            # x, y = self.get_move_coordinates()
            self.display_current_card(player)
            king_move_suggestions = suggest_king_moves(player.xPosition, player.yPosition, opponent.xPosition, opponent.
                                                       yPosition, player.player_number)
            
            # highlight the card positions for the suggested moves
            self.select_move(king_move_suggestions, player)

            # console_ui.display_valid_move(player.name, self.chosen_move, self.board)
            # console_ui.add_line_break()

        # self.board.display_board(player.xPosition, player.yPosition, opponent.xPosition, opponent.yPosition)
        # self.turn += 1
        # self.player1_turn = not self.player1_turn
        if self.is_first_move:
            self.player1_turn = not self.player1_turn
        print("Initial move completed")
        print("player 1 turn is now:", self.player1_turn)
        self.display_label()

    def handle_joker_move(self, player, opponent):
        # self.display_label(player)
        joker_suggestions = get_possible_moves_to_joker(player.xPosition, player.yPosition, self.board)

        # chosen_move = moves.choose_move_from_suggestions(joker_suggestions, self.board)

        self.highlighted_positions = joker_suggestions

        self.update_card_grid()

        # chosen_move = moves.choose_move_from_suggestions(king_move_suggestions, self.board)
        self.game_screen.wait_variable(self.is_valid_move)

        x, y = map(int, self.is_valid_move.get().split(", "))

  
        self.highlighted_positions.clear()
        if player.player_number == 1:
            self.player1.set_position(x + 1, y + 1)
        else:
            self.player2.set_position(x + 1, y + 1)
            self.update_card_grid()
            
            # console_ui.display_valid_move(player.name, (x, y), self.board)
            # console_ui.display_message("Valid move!\n{}'s new position: [{}][{}]".format(player.name,
            #                                                                              player.xPosition,
            #                                                                              player.yPosition))
            # console_ui.add_line_break()
            return True

    def handle_king_move(self, player, opponent):

        # self.display_label(player)

        king_move_suggestions = suggest_king_moves(player.xPosition, player.yPosition, opponent.xPosition, opponent.
                                                   yPosition, player.player_number)
        # chosen_move = moves.choose_move_from_suggestions(king_move_suggestions, self.board)

        self.select_move(king_move_suggestions, player)

        return True


    def handle_knight_move(self, player, opponent):
        # self.display_label(player)
        knight_move_suggestions = suggest_knight_moves(player, opponent)

        self.select_move(knight_move_suggestions, player)

        return True

    def handle_black_numeral_move(self, player, opponent):
        # self.display_label(player)

        board = self.board

        card_face = board.get_card_string(player.xPosition, player.yPosition)
        move_count = int(card_face[1:3].strip())

        black_numeral_move_suggestions = suggest_black_numeral_moves(player, move_count, opponent)
        # chosen_move = moves.choose_move_from_suggestions(black_numeral_move_suggestions, self.board)

        self.select_move(black_numeral_move_suggestions, player)

        # y = chosen_move[1]

        # if not moves.check_move(player.xPosition, y, opponent.xPosition,
        #                         opponent.yPosition, 1):
        #     console_ui.display_message("Invalid move, try again!")
        #     return False
        # else:
        #     if y == 0:
        #         console_ui.display_message("Invalid move, try again!")
        #         return False
        #     else:
        #         if player.player_number == 1:
        #             self.player1.set_position(player.xPosition, y)
        #         else:
        #             self.player2.set_position(player.xPosition, y)
        #         # console_ui.display_message("Valid move!\n{}'s new position: [{}][{}]".format(player.name,
        #         #                                                                              player.xPosition,
        #         #                                                                              player.yPosition))
        #         # console_ui.display_message('Valid Move!')
        #         # console_ui.display_message('{} chose to move to: {}'.format(player.name, chosen_move))
        #         console_ui.display_valid_move(player.name, chosen_move, self.board)

        #         console_ui.add_line_break()
        #         return True
        return True

    def handle_red_numeral_move(self, player, opponent):

        self.display_label()
        board = self.board
        card_face = board.get_card_string(player.xPosition, player.yPosition)
        move_count = int(card_face[1:3].strip())

        red_numeral_move_suggestions = suggest_red_numeral_moves(player, move_count, opponent)
        # chosen_move = moves.choose_move_from_suggestions(red_numeral_move_suggestions, self.board)
        self.select_move(red_numeral_move_suggestions, player)

        # x = chosen_move[0]

        # if not moves.check_move(x, player.yPosition, opponent.xPosition,
        #                         opponent.yPosition, 1):
        #     console_ui.display_message("Invalid move, try again!")
        #     return False
        # else:
        #     if x == 0:
        #         console_ui.display_message("Invalid move, try again!")
        #         return False
        #     else:
        #         if player.player_number == 1:
        #             self.player1.set_position(x, player.yPosition)
        #         else:
        #             self.player2.set_position(x, player.yPosition)
        #         # console_ui.display_message("Valid move!\n{}'s new position: [{}][{}]".format(player.name,
        #         #                                                                              player.xPosition,
        #         #                                                                              player.yPosition))
        #         # console_ui.display_message('Valid Move!')
        #         # console_ui.display_message('{} chose to move to: {}'.format(player.name, chosen_move))
        #         console_ui.display_valid_move(player.name, chosen_move, self.board)

        #         console_ui.add_line_break()
        #         return True
        return True

    def handle_swap_card(self, player, opponent):
        self.update_button_visibility()
        board = self.board
        joker_x, joker_y = 0, 0
        console_ui.add_line_break()
        console_ui.display_message("Choose a JOKER position...")
        self.is_joker = False

        while not self.is_joker:
            jokers_suggestions = suggest_joker_positions(self.board, self.player1, self.player2)

            chosen_joker = moves.choose_move_from_suggestions(jokers_suggestions, self.board, False)

            joker_x = chosen_joker[0]
            joker_y = chosen_joker[1]

            # handle list out of range
            card = board.get_card_string(joker_x, joker_y)

            if "JOKER" in card:
                self.is_joker = True
            else:
                console_ui.display_message("Card is not a JOKER card, try again!")

        console_ui.display_message("Choose a card position...")
        valid_move = False

        while not valid_move:

            swap_suggestions = Swap.suggest_swap_moves(joker_x, joker_y, player, opponent, moves.last_x_swap(),
                                                       moves.last_y_swap(), self.board)

            chosen_move = moves.choose_move_from_suggestions(swap_suggestions, self.board, False, True)

            x = chosen_move[0]
            y = chosen_move[1]

            if moves.last_x_swap() == x and moves.last_y_swap() == y:
                console_ui.display_message(
                    "Cannot perform swap on the same card again! Please select another card to swap..")
                valid_move = False

            elif "JOKER" in board.get_card_string(x, y):
                console_ui.display_message("Cannot perform swap of joker with joker! Please select another card to "
                                           "swap..")
                valid_move = False

            elif (x == opponent.xPosition and y == opponent.yPosition) or (joker_x == opponent.xPosition
                                                                           and joker_y ==
                                                                           opponent.yPosition) \
                    or (x == player.xPosition and y == player.yPosition) or (joker_x ==
                                                                             player.xPosition and
                                                                             joker_y ==
                                                                             player.yPosition):
                console_ui.display_message("Cannot perform swap on card occupied by self or the opponent! "
                                           "Please select another card to swap..")
                valid_move = False

            elif moves.check_swap(x, y, joker_x, joker_y):
                console_ui.display_valid_swap(player.name, (joker_x, joker_y), (x, y), self.board)
                board.card_position[joker_x][joker_y], board.card_position[x][y] = (
                    board.card_position[x][y], "[ JOKER ]")
                console_ui.add_line_break()
                moves.save_swap(joker_x, joker_y)
                valid_move = True
            else:
                console_ui.display_message("Invalid swap, try again!")
                valid_move = False

        self.on_make_move(player.player_number)

    @staticmethod
    def get_move_coordinates():
        x = int(input("X: "))
        y = int(input("Y: "))
        return x, y

    def play_with_human(self, intro_window):

        player1_name = gui.ask_player_name("Player 1", intro_window)
        player2_name = gui.ask_player_name("Player 2", intro_window)

        print('player1_name:', player1_name)
        print('player2_name:', player2_name)

        self.player1 = Player(player1_name, 1)
        self.player2 = Player(player2_name, 2)

        print('I HAVE PASSED HERE')

        intro_window.destroy()

        self.passed_welcome = True

        self.show_game_screen()

    def show_game_screen(self):

        root = self.game_screen
        root.title("Welcome to Romeo and Juliet Game")

        gui.center_window(root, 1400, 1000)

        root.deiconify()

        print('WITHOUT CLOSING HERE')

        # continue the game play here
        #UNCOM self.play_game()

    @staticmethod
    def play_with_ai():
        gui.messagebox.showinfo("Coming Soon", "Play with AI feature is coming soon!")

    def play_game(self):

        # uncomeif not self.passed_welcome:
        #     print('hello')
        #     print(self.board)

        #     # get names from the players
        #     self.request_players_info()

        #     print('IS IT HETTIGN HERE BEFORE THERE')
        # else:
        # uncome    print('WHAT NEXT HERE')

            # continue your logic bro
        self.show_game_screen()
        self.player1 = Player("Carl (Player 1)", 1)
        self.player2 = Player("Jake (Player 2)", 2)
        self.show_game_layout()

        # # Handle initial moves for both players
        self.display_label()
        self.update_button_visibility()

        # console_ui.display_message("{}'s turn for the initial move".format(self.player1.name))
        self.handle_initial_move(self.player1, self.player2)
        
        self.display_label()
        self.update_button_visibility()
        # console_ui.display_message("{}'s turn for the initial move".format(self.player2.name))
        self.handle_initial_move(self.player2, self.player1)

        # # After initial moves, continue with regular game loop
        self.is_first_move = False
        self.update_card_grid()
        self.update_button_visibility()
        
        # while not self.game_over:
        #     current_player = self.player1 if self.player1_turn else self.player2
        #     opponent = self.player2 if self.player1_turn else self.player1
        
        #     self.player1_turn = not self.player1_turn
        #     # console_ui.add_line_break()
        
        #     # console_ui.display_message("{}'s turn".format(current_player.name))
        #     self.display_current_card(current_player)
        #     # console_ui.add_line_break()
        
        #     self.handle_player_move(current_player, opponent)
        
        #     if moves.check_winning_move(current_player.xPosition, current_player.yPosition):
        #         self.game_over = True
        #         console_ui.display_message('')
        #         console_ui.add_line_break()
        #         console_ui.display_message("{} wins!".format(current_player.name))
        #         console_ui.add_line_break()
        
        #     self.player1_turn = not self.player1_turn
        #     self.board.display_board(self.player1.xPosition, self.player1.yPosition, self.player2.xPosition,
        #                              self.player2.yPosition)
        
        #     # if not self.player1_turn:  # This means Player 2 just completed their turn
        #     self.turn += 1
        # console_ui.display_message('===== Game Ended =====')
        self.game_screen.mainloop()

    def on_make_move(self, player_number):
        self.player1_turn = not self.player1_turn
        self.update_button_visibility()
        self.update_card_grid()
        # This method is triggered when a player makes a move
        current_player = self.player1 if player_number == 1 else self.player2
        # opponent = self.player2 if player_number == 1 else self.player1

        # Handle the move
        # self.handle_player_move(current_player, opponent)

        # Check if the game is over
        if moves.check_winning_move(current_player.xPosition, current_player.yPosition):
            self.game_over = True
            # Update UI to show the winning message

        if not self.game_over:
            # Switch turns
            # self.player1_turn = not self.player1_turn
            self.turn += 1
            self.update_card_grid()  #