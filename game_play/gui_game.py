import time
import tkinter as tk

from tkinter import ttk
from tkinter.font import Font
from core.classes.game_setup.board import Board
from core.classes.game_setup.card import Card
from core.classes.game_setup.pack import Pack
from core.classes.game_setup.player import Player
from core.classes.moves import moves
from core.classes.moves.black_numeral_move import best_black_numeral_move, suggest_black_numeral_moves
from core.classes.moves.joker_move import best_joker_move, suggest_joker_positions, get_possible_moves_to_joker
from core.classes.moves.king_move import best_king_move, suggest_king_moves
from core.classes.moves.knight_move import best_knight_move, suggest_knight_moves
from core.classes.moves.red_numeral_move import best_red_numeral_move, suggest_red_numeral_moves
from core.classes.moves.swap import Swap, get_best_swap
from core.enums.card_type import CardType
from interface.console import console_ui
from interface.gui import gui
from PIL import Image, ImageTk

from interface.gui.gui_interface import get_move_message, get_swap_message


class GUIGame:
    def __init__(self, board):
        self.board = board
        # players
        self.player1 = None
        self.player2 = None

        # game screen
        self.game_screen = tk.Tk()
        # hide the root window
        self.game_screen.withdraw()

        self.passed_welcome = False

        self.card_labels = [[None for _ in range(7)] for _ in range(7)]  # 7x7 grid for labels

        self.black_king = Image.open('resources/romeos/new_black_king.png').convert('RGBA')
        self.red_king = Image.open('resources/romeos/new_red_king.png').convert('RGBA')

        self.set_timer = -1
        self.turn_labels = {}  # Dictionary to store turn labels for each player
        self.timer_labels = {}
        self.is_computer_player = False
        
        self.initialize_game_state()

    def initialize_game_state(self):
        self.player1_turn = True
        self.game_over = False
        self.valid_move = False
        self.is_joker = False
        self.turn = 1
        self.is_first_move = True
        self.is_restart_game = False

        self.highlighted_positions = []
        self.chosen_move = None

        self.is_swapping_card = False

        self.last_x_swap = -1
        self.last_y_swap = -1

        self.is_valid_move = tk.StringVar()

        # self.turn_labels = {}  # Dictionary to store turn labels for each player
        self.player1_timer_seconds = 0  # For example, 10 minutes per player
        self.player2_timer_seconds = 0
        
        self.timer_task_id = None

        self.timer_enabled = False
        self.hints_enabled = False
        self.computer_move_counter = 0


    def start_timer(self):
        self.update_timer()

    def pause_timer(self):
        if self.timer_task_id is not None:
            self.game_screen.after_cancel(self.timer_task_id)
            self.timer_task_id = None

    def resume_timer(self):
        self.start_timer()

    def update_timer(self):
        current_player_timer = 'player1_timer_seconds' if self.player1_turn else 'player2_timer_seconds'
        if getattr(self, current_player_timer) > 0:
            setattr(self, current_player_timer, getattr(self, current_player_timer) - 1)

            # Calculate minutes and seconds from total seconds
            minutes, seconds = divmod(getattr(self, current_player_timer), 60)
        
            # Update the timer display for the current player with minutes and seconds
            player_number = "player1" if self.player1_turn else "player2"
            self.timer_labels[player_number].config(text=f"Time left: {minutes:02d}:{seconds:02d}", font=Font(size=12, weight='bold'))
        
            # Schedule this method to be called again after 1 second, and save the task ID
            self.timer_task_id = self.game_screen.after(1000, self.update_timer)
        else:
            self.pause_timer()
            self.end_game_due_to_timeout()

    def end_game_due_to_timeout(self):
        self.pause_timer()
        # Determine which player's time ran out and handle game end
        winner = self.player2 if self.player1_timer_seconds <= 0 else self.player1
        # gui.messagebox.showinfo("Game Over", f"Time's up! {winner} wins by timeout.")
        self.show_end_game_summary("WINNER FOUND!!! {} wins! by timeout".format(winner.name))
        # Here you can also offer the option to restart the game or exit

    def reset_game(self):
        card_pack = Pack()
        card_pack.shuffle_pack()
        self.board = Board(card_pack)  # Assuming Board is the class for the game board
        # self.initialize_game_state()
        self.initialize_game_state()
        self.is_restart_game = True
        self.passed_welcome = True
        self.timer_enabled = self.set_timer > -1
        # Update the UI to reflect the reset state
        # self.update_card_grid()
        self.display_label()
        # self.update_button_visibility()
        self.player1_timer_seconds = self.set_timer
        self.player2_timer_seconds = self.set_timer
        # self.display_label()  # Update any labels or indicators for the current turn
        self.player1.set_position(7, 1)
        self.player2.set_position(1, 7)
        # self.show_game_layout()  # Assuming this method redraws the game board
        self.update_card_grid()
        # self.handle_initial_move(self.player1, self.player2)
        self.play_game()

    def show_end_game_summary(self, title):
        summary_window = tk.Toplevel(bg='#00A550')
        summary_window.title("Game Summary")
        gui.center_window(summary_window, 1000, 800)  # Adjust size as needed

        tk.Label(summary_window, text=f"{title}", font=("Arial", 14, 'bold')).pack(pady=(50, 20))

        # Section for displaying moves
        moves_frame = tk.Frame(summary_window)
        moves_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Player 1's moves frame
        player1_frame = tk.Frame(moves_frame, bg='#00A550')
        player1_frame.pack(side="left", fill="both", expand=True)

        # Player 2's moves frame
        player2_frame = tk.Frame(moves_frame, bg='#00A550')
        player2_frame.pack(side="right", fill="both", expand=True)

        # Assuming player1.moves and player2.moves are lists of moves made by the players
        player1_moves = "\n".join(self.player1.moves)  # Placeholder
        player2_moves = "\n".join(self.player2.moves)  # Placeholder

        # Player 1's moves
        tk.Label(player1_frame, text=f"{self.player1.name}'s Moves", font=("Arial", 12), bg='#00A550', fg='white').pack(fill="x")
        tk.Label(player1_frame, text=player1_moves, justify="left", anchor="w", bg='#00A550', fg='white').pack(fill="both", expand=True)

        # Player 2's moves
        tk.Label(player2_frame, text=f"{self.player2.name}'s Moves", font=("Arial", 12), bg='#00A550', fg='white').pack(fill="x")
        tk.Label(player2_frame, text=player2_moves, justify="left", anchor="e", bg='#00A550', fg='white').pack(fill="both", expand=True)

        # Define a custom style for the buttons
        # Style configuration
        style = ttk.Style(summary_window)
        style.configure('TButton', background='white', foreground='#00A550', font=('Arial', 12, 'bold'), borderwidth=0)
        style.map('TButton', foreground=[('active', 'green')], background=[('active', 'white')])

        # Section for Restart button
        buttons_frame = tk.Frame(summary_window)
        buttons_frame.pack(fill="x", pady=(20, 10), padx=20)

        ttk.Button(buttons_frame, text="Restart Game", command=lambda: self.restart_game(summary_window), style="TButton", width=20, padding=10).pack()

        summary_window.grab_set()

        # Automatically start a new game if the summary window is closed
        # summary_window.protocol("WM_DELETE_WINDOW", self.start_new_game)

    def restart_game(self, window):
        window.destroy()  # Close the summary window
        self.reset_game()  # Use the reset logic you've already implemented

    def request_players_info(self):

        intro_window = tk.Toplevel()
        intro_window.title("Romeo and Juliet Game")

        # Set window background color
        intro_window.configure(bg='#00A550')

        gui.center_window(intro_window, 900, 900)

        text_widget = tk.Label(intro_window, text="WELCOME TO", bg='#00A550', fg='white', font=Font(size=17, weight='bold'))
        text_widget.pack(padx=10, pady=60)

        image_path = "resources/romeo_logo.png"
        img = Image.open(image_path)
        desired_width = 800
        desired_height = 300
        img = img.resize((desired_width, desired_height))

        img_tk = ImageTk.PhotoImage(img)
        label = tk.Label(intro_window, image=img_tk)
        label.configure(bg='#00A550')
        label.pack()

        # Define a custom style for the buttons
        # Style configuration
        style = ttk.Style(intro_window)
        style.configure('TButton', background='white', foreground='#00A550', font=('Arial', 12, 'bold'), borderwidth=0)
        style.map('TButton', foreground=[('active', 'green')], background=[('active', 'white')])

        play_with_human_button = ttk.Button(intro_window, text="Play with Human",
                                           command=lambda: self.play_with_human(intro_window), style="TButton", width=30, padding=10)
        play_with_ai_button = ttk.Button(intro_window, text="Play with Computer", command=lambda: self.play_with_computer(intro_window), style="TButton", width=30, padding=10)
        game_rules_button = ttk.Button(intro_window, text="Game Rules", command=gui.show_game_rules, style="TButton", width=30, padding=10)

        play_with_human_button.pack(pady=10)
        play_with_ai_button.pack(pady=10)
        game_rules_button.pack(pady=10)

        intro_window.mainloop()


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
    def create_player_section(self, parent, player_name, nomination, player_number, score):
        frame = tk.Frame(parent, bg="#00A550")

        # Define a larger font
        large_font = Font(size=12)  # Adjust the size as needed

        # Spacer at the bottom to push everything to the middle
        bottom_spacer = tk.Frame(frame, height=1, bg="#00A550")
        bottom_spacer.pack(fill='both', expand=True)

        # Player number label
        name_label = tk.Label(frame, text='Player {}'.format(player_number), anchor='center', padx=10, pady=10, bg='#00A550', fg='white')
        name_label['font'] = large_font
        name_label.pack(fill='both', pady=15)

        # Player name label 
        name_label = tk.Label(frame, text='Player Name: ', anchor='center', padx=10, bg='#00A550', fg='white')
        name_label['font'] = Font(size=10)
        name_label.pack(fill='both')
        name_label = tk.Label(frame, text=player_name, anchor='center', padx=10, pady=10)
        name_label['font'] = Font(size=14, weight='bold')
        name_label.pack(fill='both')

        # Score label
        score_label = tk.Label(frame, text='Current Score: {}'.format(score), anchor='center', padx=10, pady=10, bg='#00A550', fg='white')
        score_label['font'] = large_font
        score_label.pack(fill='both')

        # Nomination label
        nomination_label = tk.Label(frame, text=nomination, anchor='center', padx=10, pady=10, bg='#00A550', fg='white')
        nomination_label['font'] = large_font
        nomination_label.pack(fill='both')

        turn_label = tk.Label(frame, text="", anchor='center', padx=0, pady=0, width=20, wraplength=150, bg='#00A550', fg='white')
        turn_label['font'] = Font(size=8)
        turn_label.pack(fill='both')
        self.turn_labels[player_number] = turn_label

        # Define a custom style for the buttons
        # Style configuration
        style = ttk.Style(frame)
        style.configure('TButton', background='white', foreground='#00A550', font=('Arial', 12, 'bold'), borderwidth=0)
        style.map('TButton', foreground=[('active', 'green')], background=[('active', 'white')])

        # Buttons with color
        # Button to make a move
        move_button = ttk.Button(frame, text="Make a Move",
                                command=lambda: self.move_card(),style="TButton", width=20, padding=10)

        # Button to swap a card
        swap_button = ttk.Button(frame, text="Swap a Card", 
                                command=lambda: self.swap_card(),style="TButton", width=20, padding=10)
        
        # self.setup_restart_button()
        restart_button = ttk.Button(frame, text="Restart Game", command=self.reset_game,style="TButton", width=20, padding=10)
        restart_button.pack(pady=10)

        if self.timer_enabled:

            # Calculate minutes and seconds from total seconds for initial display
            total_seconds = getattr(self, f'player{player_number}_timer_seconds')
            minutes, seconds = divmod(total_seconds, 60)

            timer_label = tk.Label(frame, text=f"Time left: {minutes:02d}:{seconds:02d}")
            timer_label['font'] = Font(size=8)
            timer_label.pack()
            self.timer_labels[f'player{player_number}'] = timer_label


        # Store references to the buttons
        if player_number == 1:
            self.player1_move_button = move_button
            self.player1_swap_button = swap_button
        else:
            self.player2_move_button = move_button
            self.player2_swap_button = swap_button

        # Spacer at the bottom to push everything to the middle
        bottom_spacer = tk.Frame(frame, height=1, bg="#00A550")
        bottom_spacer.pack(fill='both', expand=True)

        return frame

    def display_label(self):
        self.turn_labels[1].config(font=Font(size=12, weight='bold'))
        self.turn_labels[2].config(font=Font(size=12, weight='bold'))
        # is_player_1 = player.player_number == 1
        p = self.player1 if self.player1_turn else self.player2
        if self.is_first_move:
            # self.turn_labels[1].config(text="{}'s - {} Turn for the initial move".format(p.name, p.currentScore))
            self.turn_labels[1].config(text="{}'s initial move".format(p.name))
            self.turn_labels[2].config(text="{}'s initial move".format(p.name))
            # self.turn_labels[2].config(text="{}'s - {} Turn for the initial move".format(p.name, p.currentScore))
        else:
            # self.turn_labels[1].config(text="")
            # self.turn_labels[2].config(text="")
            # self.turn_labels[1].config(text="{}'s - {} Turn to make a move or swap a card".format(p.name, p.currentScore))
            self.turn_labels[1].config(text="{}'s Turn".format(p.name))
            self.turn_labels[2].config(text="{}'s Turn".format(p.name))
            # self.turn_labels[2].config(text="{}'s - {} Turn to make a move or swap a card".format(p.name, p.currentScore))

        self.turn_labels[1].pack(fill='both')
        self.turn_labels[2].pack(fill='both')

    def update_card_grid(self):
        print("Updating the card grid => hightlighted positions:", self.highlighted_positions)
        card_width, card_height = 110, 125  # Set the dimensions for the card images

        for i in range(1, 8):
            for j in range(1, 8):
                grid_i = i - 1  # Adjusting for zero-indexed list
                grid_j = j - 1
                # Reset the label configurations and unbind previous events
                self.card_labels[grid_i][grid_j].config(image='', highlightthickness=0, highlightbackground=None)
                self.card_labels[grid_i][grid_j].unbind("<Button-1>")

                if (i, j) == (1, 7):  # Top left position for red queen
                    card_image_path = 'resources/card_images/queen_of_hearts.png'
                elif (i, j) == (7, 1):  # Bottom left position for black queen
                    card_image_path = 'resources/card_images/queen_of_spades.png'
                else:
                    card_image_path = self.board.get_card_image(grid_i + 1, grid_j + 1)  # Assuming 1-indexed positions

                if card_image_path and card_image_path != "No card at this position":
                    img = Image.open(card_image_path)
                    img = img.resize((card_width, card_height), Image.BOX)

                    if (i, j) == (self.player1.xPosition, self.player1.yPosition):
                        king_img = self.red_king
                        king_width, king_height = king_img.size
                        x = (card_width - king_width) // 2
                        y = (card_height - king_height) // 2
                        img.paste(king_img, (x, y), king_img)
                    elif (i, j) == (self.player2.xPosition, self.player2.yPosition):
                        king_img = self.black_king
                        king_width, king_height = king_img.size
                        x = (card_width - king_width) // 2
                        y = (card_height - king_height) // 2
                        img.paste(king_img, (x, y), king_img)

                    card_image = ImageTk.PhotoImage(img)
                else:
                    card_image = None

                if card_image:  # Only configure the label if there's an image
                    self.card_labels[grid_i][grid_j].config(image=card_image)
                    self.card_labels[grid_i][grid_j].image = card_image  # Keep a reference
                else:
                    self.card_labels[grid_i][grid_j].config(image='')  # Clear the image for empty cells

                position = (i, j)
                if position in self.highlighted_positions:
                    king_img = self.black_king if (i, j) == (
                    self.player1.xPosition, self.player1.yPosition) else self.red_king
                    color = 'red' if self.player1_turn else 'black'
                    self.card_labels[grid_i][grid_j].config(highlightthickness=5, highlightbackground=color)
                    self.card_labels[grid_i][grid_j].bind("<Button-1>",
                                                          lambda e, x=grid_i, y=grid_j: self.on_card_click(x, y, True))
                else:
                    self.card_labels[grid_i][grid_j].bind("<Button-1>",
                                                          lambda e, x=grid_i, y=grid_j: self.on_card_click(x, y, False))

                self.card_labels[grid_i][grid_j].grid(row=grid_i, column=grid_j, sticky='nswe', padx=5, pady=5)

    def show_game_layout(self):
        root = self.game_screen

        main_frame = tk.Frame(root, bg="white")
        main_frame.pack(fill="both", expand=True)

        # Section 1 - Player 1
        player1_frame = self.create_player_section(main_frame, self.player1.name, "RED PLAYER", 1, self.player1.currentScore)
        player1_frame.pack(side="left", fill="both", expand=True, anchor="center")

        # Section 2 - Card Grid (7x7)
        # Section 2 - Card Grid (7x7)
        # Initialize a 7x7 grid of Labels to hold card images
        card_frame = tk.Frame(main_frame, bg="#00A550")
        card_frame.pack(side="left", fill="both", expand=True, anchor="center")
        
        # Section 3 - Player 2
        player2_frame = self.create_player_section(main_frame, self.player2.name, "BLACK PLAYER", 2, self.player2.currentScore)
        player2_frame.pack(side="left", fill="both", expand=True, anchor="center")

        card_width = 110
        card_height = 125

                # Initialize a 7x7 grid of Labels to hold card images
        self.card_labels = [[tk.Label(card_frame) for _ in range(7)] for _ in range(7)]
        for i in range(1, 8):
            for j in range(1, 8):
                grid_i = i - 1  # Adjusting for zero-indexed list
                grid_j = j - 1
                if (i, j) == (1, 7):  # Top left position for red queen
                    card_image_path = 'resources/card_images/queen_of_hearts.png'
                elif (i, j) == (7, 1):  # Bottom left position for black queen
                    card_image_path = 'resources/card_images/queen_of_spades.png'
                else:
                    # Get the image for the card at the current position
                    card_image_path = self.board.get_card_image(grid_i + 1, grid_j + 1)  # Assuming 1-indexed positions

                if card_image_path and card_image_path != "No card at this position":
                    # Open the image file
                    img = Image.open(card_image_path)
                    # Resize the image
                    img = img.resize((card_width, card_height), Image.BOX)

                    if (i, j) in [(self.player1.xPosition, self.player1.yPosition),
                                  (self.player2.xPosition, self.player2.yPosition)]:
                        king_img = self.black_king if (i, j) == (
                        self.player1.xPosition, self.player1.yPosition) else self.red_king
                        king_width, king_height = king_img.size
                        x = (card_width - king_width) // 2
                        y = (card_height - king_height) // 2
                        img.paste(king_img, (x, y), king_img)

                    card_image = ImageTk.PhotoImage(img)
                else:
                    # You might want to have a default image for empty spaces or a placeholder
                    card_image = None  # Placeholder for an empty image

                if card_image:  # Only configure the label if there's an image
                    self.card_labels[grid_i][grid_j].config(image=card_image)
                    self.card_labels[grid_i][grid_j].image = card_image  # Keep a reference
                self.card_labels[grid_i][grid_j].grid(row=grid_i, column=grid_j, sticky='nswe')

                position = (i + 1, j + 1)
                color = 'red' if self.player1_turn else 'black'
                if position in self.highlighted_positions:
                    self.card_labels[grid_i][grid_j].config(highlightthickness=5, highlightbackground=color)
                    self.card_labels[grid_i][grid_j].bind("<Button-1>",
                                                          lambda e, x=grid_i, y=grid_j: self.on_card_click(x, y, True))
                else:
                    self.card_labels[grid_i][grid_j].bind("<Button-1>",
                                                          lambda e, x=grid_i, y=grid_j: self.on_card_click(x, y, False))
        # Configure the grid weight
      #  root.grid_rowconfigure(0, weight=1)

       # for i in range(7):
         #   root.grid_columnconfigure(i, weight=1)
          #  card_frame.grid_rowconfigure(i, weight=1)
            #card_frame.grid_columnconfigure(i, weight=1)

        # Player sections weight configuration
     #   root.grid_columnconfigure(0, weight=1)
        #root.grid_columnconfigure(8, weight=1)

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
            print(f"Clicked on a valid card at position ({x + 1}, {y + 1})")
            # Perform necessary actions for a valid move
            # Update player positions, etc.
            # self.valid_move = (x, y)
            self.is_valid_move.set(f"{x}, {y}")
        else:
            print(f"Clicked on an invalid card at position ({x + 1}, {y + 1})")
            # Handle invalid move (show message, etc.)
            gui.messagebox.showinfo("Invalid Move", "The card selected cannot be moved to!")

    def handle_player_move(self, player, opponent):

        if self.is_first_move:
            self.handle_initial_move(player, opponent)

        else:
            self.handle_move_card(player, opponent)

    def display_current_card(self, player):
        card_face = self.board.get_card_string(player.xPosition, player.yPosition)
        console_ui.add_line_break()
        console_ui.display_message("{} is currently on: {}".format(player.name, card_face))

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

        self.game_screen.wait_variable(self.is_valid_move)

        x, y = map(int, self.is_valid_move.get().split(", "))

        # update the moves for the player
        player.moves.append(get_move_message(player.name, (x+1, y+1), self.board))
        print(player.moves)

        self.valid_move = True

        self.highlighted_positions.clear()

        if player.player_number == 1:
            self.player1.set_position(x + 1, y + 1)
        else:
            self.player2.set_position(x + 1, y + 1)

        self.update_card_grid()
    
    def handle_computer_move(self, x, y):
        self.computer_move_counter +=1
        self.player2.moves.append(get_move_message(self.player2.name, (x, y), self.board))
        print(self.player2.moves)
        self.valid_move = True
        self.player2.set_position(x, y)
        self.update_card_grid()

    def handle_computer_swap(self, x, y, joker_x, joker_y):
        board = self.board

        self.computer_move_counter +=1
        self.player2.moves.append(get_swap_message(self.player2.name, (x-1, y), (joker_x-1, joker_y), self.board))
        print(self.player2.moves)
        self.valid_move = True

        self.board.card_position[joker_x][joker_y] = board.card_position[x][y]
        self.board.card_position[x][y] = Card(None, None, CardType.JOKER)

        self.last_x_swap = joker_x
        self.last_y_swap = joker_y
        
        # self.player2.set_position(x, y)
        self.update_card_grid()
        self.on_make_move(2)

    def handle_initial_move(self, player, opponent):
        if self.is_computer_player and player.player_number == 2:
            x, y = best_king_move(player.xPosition, player.yPosition, opponent.xPosition, opponent.yPosition, 7, 1,
                                  player.player_number)
            self.handle_computer_move(x, y)
            self.player1_turn = not self.player1_turn
            self.display_label()
            self.is_first_move = False
            return

        self.valid_move = False

        while not self.valid_move:
            self.display_current_card(player)
            king_move_suggestions = suggest_king_moves(player.xPosition, player.yPosition, opponent.xPosition, opponent.
                                                       yPosition, player.player_number)

            # highlight the card positions for the suggested moves
            self.select_move(king_move_suggestions, player)

        if self.is_first_move:
            if self.timer_enabled:
                self.pause_timer()
            self.player1_turn = not self.player1_turn
            if self.timer_enabled:
                self.resume_timer()
        print("Initial move completed")
        print("player 1 turn is now:", self.player1_turn)
        self.display_label()

    def handle_joker_move(self, player, opponent):
        if self.is_computer_player and player.player_number == 2:
            x, y = best_joker_move(player.xPosition, player.yPosition, self.board, (opponent.xPosition, opponent.yPosition))
            self.handle_computer_move(x, y)
            return True

        joker_suggestions = get_possible_moves_to_joker(player.xPosition, player.yPosition, self.board)

        self.highlighted_positions = joker_suggestions

        self.update_card_grid()

        self.game_screen.wait_variable(self.is_valid_move)

        x, y = map(int, self.is_valid_move.get().split(", "))

        self.highlighted_positions.clear()
        if player.player_number == 1:
            self.player1.set_position(x + 1, y + 1)
        else:
            self.player2.set_position(x + 1, y + 1)
            self.update_card_grid()

            return True

    def handle_king_move(self, player, opponent):

        if self.is_computer_player and player.player_number == 2:
            x, y = best_king_move(player.xPosition, player.yPosition, opponent.xPosition, opponent.yPosition, 7, 1,
                                  player.player_number)
            self.handle_computer_move(x, y)
            return True
        
        king_move_suggestions = suggest_king_moves(player.xPosition, player.yPosition, opponent.xPosition, opponent.
                                                   yPosition, player.player_number)

        self.select_move(king_move_suggestions, player)

        return True

    def handle_knight_move(self, player, opponent):
        if self.is_computer_player and player.player_number == 2:
            x, y = best_knight_move(player, opponent, (7, 1))
            self.handle_computer_move(x, y)
            return True
        
        knight_move_suggestions = suggest_knight_moves(player, opponent)

        self.select_move(knight_move_suggestions, player)

        return True

    def handle_black_numeral_move(self, player, opponent):
                
        board = self.board

        card_face = board.get_card_string(player.xPosition, player.yPosition)
        move_count = int(card_face[1:3].strip())

        if self.is_computer_player and player.player_number == 2:
            x, y = best_black_numeral_move(player, move_count, opponent, (7, 1))
            self.handle_computer_move(x, y)
            return True


        black_numeral_move_suggestions = suggest_black_numeral_moves(player, move_count, opponent)

        self.select_move(black_numeral_move_suggestions, player)
        return True

    def handle_red_numeral_move(self, player, opponent):

        self.display_label()
        board = self.board
        card_face = board.get_card_string(player.xPosition, player.yPosition)
        move_count = int(card_face[1:3].strip())

        if self.is_computer_player and player.player_number == 2:
            x, y = best_red_numeral_move(player, move_count, opponent, (7,1))
            self.handle_computer_move(x, y)
            return True


        red_numeral_move_suggestions = suggest_red_numeral_moves(player, move_count, opponent)
        self.select_move(red_numeral_move_suggestions, player)

        return True

    def handle_swap_card(self, player, opponent):
        if self.is_computer_player and player.player_number == 2:
            joker_positions = suggest_joker_positions(self.board, self.player1, self.player2)

            best_swap, best_joker = get_best_swap(joker_positions, player, opponent, self.last_x_swap, self.last_y_swap, self.board)
            x, y = best_swap
            joker_x, joker_y = best_joker

            self.handle_computer_swap(x, y, joker_x, joker_y)
            return
        
        board = self.board
        joker_x, joker_y = 0, 0

        if self.player1_turn:
            self.turn_labels[1].config(text="Select a Joker card you want to swap with!")
        else:
            self.turn_labels[2].config(text="Select a Joker card you want to swap with!")

        self.is_swapping_card = True
        self.is_joker = False

        while not self.is_joker:
            jokers_suggestions = suggest_joker_positions(self.board, self.player1, self.player2)

            # chosen_joker = moves.choose_move_from_suggestions(jokers_suggestions, self.board, False)
            self.highlighted_positions = jokers_suggestions

            self.update_card_grid()

            self.game_screen.wait_variable(self.is_valid_move)

            jx, jy = map(int, self.is_valid_move.get().split(", "))

            joker_x = jx + 1
            joker_y = jy + 1

            # handle list out of range
            card = self.board.get_card_string(joker_x, joker_y)
            print("card at this place is ", card)

            if "JOKER" in card:
                self.is_joker = True
                self.highlighted_positions.clear()
            else:
                gui.messagebox.showinfo("Invalid Selection", "Card is not a JOKER card, try again!")

        if self.player1_turn:
            self.turn_labels[1].config(text="Select a Card you want to swap with!")
        else:
            self.turn_labels[2].config(text="Select a Card you want to swap with!")

        valid_move = False

        while not valid_move:

            swap_suggestions = Swap.suggest_swap_moves(joker_x, joker_y, player, opponent, moves.last_x_swap(),
                                                       moves.last_y_swap(), self.board)

            self.highlighted_positions = swap_suggestions

            self.update_card_grid()

            self.game_screen.wait_variable(self.is_valid_move)

            x, y = map(int, self.is_valid_move.get().split(", "))
            x = x + 1
            y = y + 1

            print("last swap is at", self.last_x_swap, self.last_y_swap)
            print("X and Y is at", x, y)

            if self.last_x_swap == x and self.last_y_swap == y:
                gui.messagebox.showinfo("Invalid Selection",
                                        "Cannot perform swap on the same card again! Please select another card to "
                                        "swap..")
                valid_move = False

            elif "JOKER" in board.get_card_string(x, y):
                gui.messagebox.showinfo("Invalid Selection",
                                        "Cannot perform swap of joker with joker! Please select another card to "
                                        "swap..")

                valid_move = False

            elif (x == opponent.xPosition and y == opponent.yPosition) or (joker_x == opponent.xPosition
                                                                           and joker_y ==
                                                                           opponent.yPosition) \
                    or (x == player.xPosition and y == player.yPosition) or (joker_x ==
                                                                             player.xPosition and
                                                                             joker_y ==
                                                                             player.yPosition):
                gui.messagebox.showinfo("Invalid Selection",
                                        "Cannot perform swap on card occupied by self or the opponent! "
                                        "Please select another card to swap..")
                valid_move = False

            elif moves.check_swap(x, y, joker_x, joker_y):
                print("Card position is at ", x, y)
                print("Joker position is at ", joker_x, joker_y)

                # update the moves for the player
                player.moves.append(get_swap_message(player.name, (joker_x, joker_y), (x, y), self.board))
                print(player.moves)

                self.board.card_position[joker_x][joker_y] = board.card_position[x][y]
                self.board.card_position[x][y] = Card(None, None, CardType.JOKER)

                self.last_x_swap = joker_x
                self.last_y_swap = joker_y

                # console_ui.add_line_break()
                if self.player1_turn:
                    self.turn_labels[1].config(text="Valid swap!!!")
                else:
                    self.turn_labels[2].config(text="Valid swap!!!")

                self.highlighted_positions.clear()

                self.update_card_grid()

                valid_move = True
            else:
                gui.messagebox.showinfo("Invalid swap, try again!")
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


        self.passed_welcome = True

        # ask for the details here (show hints and game timer)

        # self.show_game_screen()
        def on_game_options_selected(timer_enabled, hints_enabled, timer_minutes):
            print(f"Timer Enabled: {timer_enabled}")
            self.timer_enabled = timer_enabled
            print(f"Hints Enabled: {hints_enabled}")
            self.hints_enabled = hints_enabled
            print(f"Timer Minutes: {timer_minutes}")
            self.set_timer = int(timer_minutes) * 60
            self.player1_timer_seconds = int(timer_minutes) * 60
            self.player2_timer_seconds = int(timer_minutes) * 60
            # Now you can set up the game with these options
            # self.start_game_with_options(timer_enabled, hints_enabled, timer_minutes)
            intro_window.destroy()
        
            self.show_game_screen()

        self.ask_game_options(intro_window, on_game_options_selected)

    def ask_game_options(self, parent_window, callback):
        options_window = tk.Toplevel(parent_window)
        options_window.title("Game Options")
        gui.center_window(options_window, 300, 200)  # Adjust size as needed

        timer_var = tk.BooleanVar(value=False)
        hints_var = tk.BooleanVar(value=False)

        # Label and Checkbutton for timer
        timer_label = tk.Label(options_window, text="Enable Timer?")
        timer_label.pack()
        timer_checkbutton = tk.Checkbutton(options_window, text="Yes", variable=timer_var, command=lambda: self.toggle_timer_entry(timer_entry, timer_label_minutes, timer_var))
        timer_checkbutton.pack()

        # Label and Entry for timer minutes; initially not visible
        timer_label_minutes = tk.Label(options_window, text="Timer in minutes")
        timer_entry = tk.Entry(options_window)

        # Label and Checkbutton for hints
        hints_label = tk.Label(options_window, text="Enable Hints?")
        hints_label.pack()
        hints_checkbutton = tk.Checkbutton(options_window, text="Yes", variable=hints_var)
        hints_checkbutton.pack()

        def on_confirm():
            timer_enabled = timer_var.get()
            hints_enabled = hints_var.get()
            timer_minutes = timer_entry.get() if timer_enabled else "0"
            callback(timer_enabled, hints_enabled, timer_minutes)
            options_window.destroy()

        confirm_button = tk.Button(options_window, text="Confirm", command=on_confirm)
        confirm_button.pack()

    def toggle_timer_entry(self, timer_entry, timer_label, timer_var):
        if timer_var.get():
            # Show timer entry and label if timer is enabled
            timer_label.pack()
            timer_entry.pack()
        else:
            # Hide timer entry and label if timer is not enabled
            timer_label.pack_forget()
            timer_entry.pack_forget()

    def show_game_screen(self):

        root = self.game_screen
        root.title("Welcome to Romeo and Juliet Game")

        gui.center_window(root, 1300, 1000)

        root.deiconify()

        # continue the game play here
        self.play_game()

    def play_with_computer(self, intro_window):
        self.is_computer_player = True
        player1_name = gui.ask_player_name("Player 1", intro_window)

        print('player1_name:', player1_name)
        self.player1 = Player(player1_name, 1)
        self.player2 = Player('Computer Player', 2)

        self.passed_welcome = True

        #self.show_game_screen()

        def on_game_options_selected(timer_enabled, hints_enabled, timer_minutes):
            print(f"Timer Enabled: {timer_enabled}")
            self.timer_enabled = timer_enabled
            print(f"Hints Enabled: {hints_enabled}")
            self.hints_enabled = hints_enabled
            print(f"Timer Minutes: {timer_minutes}")
            self.set_timer = int(timer_minutes) * 60
            self.player1_timer_seconds = int(timer_minutes) * 60
            self.player2_timer_seconds = int(timer_minutes) * 60
            # Now you can set up the game with these options
            # self.start_game_with_options(timer_enabled, hints_enabled, timer_minutes)
            intro_window.destroy()
        
            self.show_game_screen()

        self.ask_game_options(intro_window, on_game_options_selected)

    def on_make_move(self, player_number):
        if self.timer_enabled:
            self.pause_timer()
        self.player1_turn = not self.player1_turn
        if self.timer_enabled:
            self.resume_timer()
        self.update_button_visibility()
        self.update_card_grid()
        self.display_label()

        # This method is triggered when a player makes a move
        current_player = self.player1 if player_number == 1 else self.player2
        # opponent = self.player2 if player_number == 1 else self.player1

        # Handle the move
        # self.handle_player_move(current_player, opponent)

        # Check if the game is over
        if moves.check_winning_move(current_player.xPosition, current_player.yPosition):
            self.game_over = True
            if self.timer_enabled:
                self.pause_timer()
            # Update UI to show the winning message
            self.show_end_game_summary("WINNER FOUND!!! {} wins the game!".format(current_player.name))


            # end game summary
            # display the total number of moves made by each player
            # display the list of moves made by each player
            # display who won the game

            # update the score of the current player
            current_player.currentScore = current_player.currentScore + 1

        if not self.game_over:
            # Switch turns
            # self.player1_turn = not self.player1_turn
            self.turn += 1
            self.update_card_grid()  #

            # wait for 2 seconds before making the computer move
            if self.is_computer_player and not self.player1_turn:
                # time.sleep(2)
                # self.handle_move_card(self.player2, self.player1)
                # make the computer make a swap after 5 moves
                if self.computer_move_counter >= 5:
                # if self.computer_move_counter >= 5:
                    self.computer_move_counter = 0
                    self.game_screen.after(1000, self.handle_swap_card(self.player2, self.player1))
                    self.display_label()
                else:
                    self.game_screen.after(1000, self.handle_move_card, self.player2, self.player1)
                    self.display_label()

    def play_game(self):

        if not self.passed_welcome:

            # get names from the players
            self.request_players_info()

        else:
            if (not self.is_restart_game):
                self.show_game_layout()

            if self.timer_enabled: 
                self.update_timer()

            # Handle initial moves for both players
            self.display_label()
            self.update_button_visibility()

            self.handle_initial_move(self.player1, self.player2)

            self.display_label()
            self.update_button_visibility()

            self.handle_initial_move(self.player2, self.player1)
            
            self.display_label()


            # After initial moves, continue with regular game loop
            self.is_first_move = False
            self.update_card_grid()
            self.update_button_visibility()

        self.game_screen.mainloop()
