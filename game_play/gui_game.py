import tkinter as tk

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

    # Define the player sections
    @staticmethod
    def create_player_section(parent, player_name, nomination):
        frame = tk.Frame(parent)
        name_label = tk.Label(frame, text=player_name, anchor='center', padx=10, pady=10)
        name_label.pack(fill='both')
        nomination_label = tk.Label(frame, text=nomination, anchor='center', padx=10, pady=10)
        nomination_label.pack(fill='both')

        # only show this if it is the players turn
        # "Your turn" label
        turn_label = tk.Label(frame, text="Your turn", anchor='center', padx=10, pady=10)
        turn_label.pack(fill='both')

        # Buttons
        button1 = tk.Button(frame, text="Make a Move")
        button1.pack(side=tk.LEFT, padx=5, pady=10)
        button2 = tk.Button(frame, text="Swap a Card")
        button2.pack(side=tk.RIGHT, padx=5, pady=10)

        return frame

    def show_game_layout(self):
        root = self.game_screen

        # Section 1 - Player 1
        player1_frame = self.create_player_section(root, self.player1.name, "RED PLAYER")
        player1_frame.grid(row=0, column=0, sticky='nswe')

        # Section 3 - Player 2
        player2_frame = self.create_player_section(root, self.player2.name, "BLACK PLAYER")
        player2_frame.grid(row=0, column=8, sticky='nswe')

        # Section 2 - Card Grid (7x7)
        # Section 2 - Card Grid (7x7)
        # Initialize a 7x7 grid of Labels to hold card images
        card_frame = tk.Frame(root)
        card_frame.grid(row=0, column=1, columnspan=7, sticky='nswe')

        self.card_labels = [[tk.Label(card_frame) for _ in range(7)] for _ in range(7)]
        for i in range(7):
            for j in range(7):
                # Get the image for the card at the current position
                card_image_path = self.board.get_card_image(i + 1, j + 1)  # Assuming 1-indexed positions
                if card_image_path and card_image_path != "No card at this position":
                    card_image = tk.PhotoImage(file=card_image_path)
                else:
                    # You might want to have a default image for empty spaces or a placeholder
                    card_image = tk.PhotoImage()  # Placeholder for an empty image

                self.card_labels[i][j].config(image=card_image)
                self.card_labels[i][j].image = card_image  # Keep a reference
                self.card_labels[i][j].grid(row=i, column=j, sticky='nswe', padx=5, pady=5)

        # Configure the grid weight
        root.grid_rowconfigure(0, weight=1)

        for i in range(7):
            root.grid_columnconfigure(i + 1, weight=1)
            card_frame.grid_rowconfigure(i, weight=1)
            card_frame.grid_columnconfigure(i, weight=1)

        # Player sections weight configuration
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(8, weight=1)

        # Label inputs below the card grid
        input_frame = tk.Frame(root)
        input_frame.grid(row=1, column=1, columnspan=7, pady=20)

        label_inputs = ['Label 1', 'Label 2', 'Label 3', 'Label 4']
        entries = []
        for idx, label in enumerate(label_inputs):
            tk.Label(input_frame, text=label).grid(row=0, column=idx, padx=10)
            entry = tk.Entry(input_frame)
            entry.grid(row=1, column=idx, padx=10)
            entries.append(entry)

    def handle_player_move(self, player, opponent):

        if self.is_first_move:
            self.handle_initial_move(player, opponent)

        else:
            # console_ui.display_message("\n<Move {}>".format(self.turn))
            choice = console_ui.turn_choice()

            if choice == 1:
                self.handle_move_card(player, opponent)
            elif choice == 2:
                self.handle_swap_card(player, opponent)

    def display_current_card(self, player):
        card_face = self.board.get_card_string(player.xPosition, player.yPosition)
        console_ui.add_line_break()
        console_ui.display_message("{} is currently on: {}".format(player.name, card_face))

    def handle_move_card(self, player, opponent):
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

    def handle_initial_move(self, player, opponent):
        self.valid_move = False

        while not self.valid_move:
            # x, y = self.get_move_coordinates()
            self.display_current_card(player)
            king_move_suggestions = suggest_king_moves(player.xPosition, player.yPosition, opponent.xPosition, opponent.
                                                       yPosition, player.player_number)
            chosen_move = moves.choose_move_from_suggestions(king_move_suggestions, self.board)

            self.valid_move = True

            x = chosen_move[0]
            y = chosen_move[1]

            if player.player_number == 1:
                self.player1.set_position(x, y)
            else:
                self.player2.set_position(x, y)

            console_ui.display_valid_move(player.name, chosen_move, self.board)
            console_ui.add_line_break()

        self.board.display_board(player.xPosition, player.yPosition, opponent.xPosition, opponent.yPosition)
        self.turn += 1

    def handle_joker_move(self, player, opponent):
        joker_suggestions = get_possible_moves_to_joker(player.xPosition, player.yPosition, self.board)

        chosen_move = moves.choose_move_from_suggestions(joker_suggestions, self.board)

        x = chosen_move[0]
        y = chosen_move[1]

        if not moves.check_move(x, y, opponent.xPosition, opponent.yPosition, player.player_number):
            console_ui.display_message("Invalid move, try again!")
            return False
        elif moves.joker_move(player.xPosition, player.yPosition, x, y):
            if player.player_number == 1:
                self.player1.set_position(x, y)
            else:
                self.player2.set_position(x, y)
            console_ui.display_valid_move(player.name, (x, y), self.board)
            # console_ui.display_message("Valid move!\n{}'s new position: [{}][{}]".format(player.name,
            #                                                                              player.xPosition,
            #                                                                              player.yPosition))
            console_ui.add_line_break()
            return True
        else:
            console_ui.display_message("Invalid move, try again!")
            return False

    def handle_king_move(self, player, opponent):
        king_move_suggestions = suggest_king_moves(player.xPosition, player.yPosition, opponent.xPosition, opponent.
                                                   yPosition, player.player_number)
        chosen_move = moves.choose_move_from_suggestions(king_move_suggestions, self.board)

        console_ui.display_message('{} chose to move to: {}'.format(player.name, chosen_move))

        x = chosen_move[0]
        y = chosen_move[1]
        if not moves.check_move(x, y, opponent.xPosition, opponent.yPosition, player.player_number):
            console_ui.display_message("Invalid move, try again!")
            return False

        elif moves.king_move(player.xPosition, player.yPosition, x, y):
            if player.player_number == 1:
                self.player1.set_position(x, y)
            else:
                self.player2.set_position(x, y)
            # console_ui.display_message('Valid Move!')
            # console_ui.display_message("Valid move!\n{}'s new position: [{}][{}]".format(player.name,
            #                                                                              player.xPosition,
            #                                                                              player.yPosition))
            # console_ui.display_message('{} chose to move to: {}'.format(player.name, chosen_move))
            console_ui.display_valid_move(player.name, chosen_move, self.board)
            console_ui.add_line_break()
            return True
        else:
            console_ui.display_message("Invalid move, try again!")
            return False

    def handle_knight_move(self, player, opponent):
        knight_move_suggestions = suggest_knight_moves(player, opponent)

        chosen_move = moves.choose_move_from_suggestions(knight_move_suggestions, self.board)
        x = chosen_move[0]
        y = chosen_move[1]

        if not moves.check_move(x, y, opponent.xPosition, opponent.yPosition, player.player_number):
            print("Invalid move, try again!")
            return False
        elif moves.knight_move(player.xPosition, player.yPosition, x, y):
            if player.player_number == 1:
                self.player1.set_position(x, y)
            else:
                self.player2.set_position(x, y)
                # console_ui.display_message("Valid move!\n{}'s new position: [{}][{}]".format(player.name,
                #                                                                              player.xPosition,
                #                                                                              player.yPosition))
                # console_ui.display_message('Valid Move!')
                # console_ui.display_message('{} chose to move to: {}'.format(player.name, chosen_move))
                console_ui.display_valid_move(player.name, chosen_move, self.board)

                console_ui.add_line_break()
            return True
        else:
            console_ui.display_message("Invalid move, try again!")
            return False

    def handle_black_numeral_move(self, player, opponent):
        board = self.board

        card_face = board.get_card_string(player.xPosition, player.yPosition)
        move_count = int(card_face[1:3].strip())

        black_numeral_move_suggestions = suggest_black_numeral_moves(player, move_count, opponent)
        chosen_move = moves.choose_move_from_suggestions(black_numeral_move_suggestions, self.board)

        y = chosen_move[1]

        if not moves.check_move(player.xPosition, y, opponent.xPosition,
                                opponent.yPosition, 1):
            console_ui.display_message("Invalid move, try again!")
            return False
        else:
            if y == 0:
                console_ui.display_message("Invalid move, try again!")
                return False
            else:
                if player.player_number == 1:
                    self.player1.set_position(player.xPosition, y)
                else:
                    self.player2.set_position(player.xPosition, y)
                # console_ui.display_message("Valid move!\n{}'s new position: [{}][{}]".format(player.name,
                #                                                                              player.xPosition,
                #                                                                              player.yPosition))
                # console_ui.display_message('Valid Move!')
                # console_ui.display_message('{} chose to move to: {}'.format(player.name, chosen_move))
                console_ui.display_valid_move(player.name, chosen_move, self.board)

                console_ui.add_line_break()
                return True

    def handle_red_numeral_move(self, player, opponent):
        board = self.board
        card_face = board.get_card_string(player.xPosition, player.yPosition)
        move_count = int(card_face[1:3].strip())

        red_numeral_move_suggestions = suggest_red_numeral_moves(player, move_count, opponent)
        chosen_move = moves.choose_move_from_suggestions(red_numeral_move_suggestions, self.board)

        x = chosen_move[0]

        if not moves.check_move(x, player.yPosition, opponent.xPosition,
                                opponent.yPosition, 1):
            console_ui.display_message("Invalid move, try again!")
            return False
        else:
            if x == 0:
                console_ui.display_message("Invalid move, try again!")
                return False
            else:
                if player.player_number == 1:
                    self.player1.set_position(x, player.yPosition)
                else:
                    self.player2.set_position(x, player.yPosition)
                # console_ui.display_message("Valid move!\n{}'s new position: [{}][{}]".format(player.name,
                #                                                                              player.xPosition,
                #                                                                              player.yPosition))
                # console_ui.display_message('Valid Move!')
                # console_ui.display_message('{} chose to move to: {}'.format(player.name, chosen_move))
                console_ui.display_valid_move(player.name, chosen_move, self.board)

                console_ui.add_line_break()
                return True

    def handle_swap_card(self, player, opponent):
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

        gui.center_window(root, 1600, 1200)

        root.deiconify()

        print('WITHOUT CLOSING HERE')

        # continue the game play here
        self.play_game()

    @staticmethod
    def play_with_ai():
        gui.messagebox.showinfo("Coming Soon", "Play with AI feature is coming soon!")

    def play_game(self):

        if not self.passed_welcome:
            print('hello')
            print(self.board)

            # get names from the players
            self.request_players_info()

            print('IS IT HETTIGN HERE BEFORE THERE')
        else:
            print('WHAT NEXT HERE')

            # continue your logic bro
            self.show_game_layout()

        # destroy all the buttons and show the board
        # play_with_human_button.destroy()
        # play_with_ai_button.destroy()
        # game_rules_button.destroy()

        # image_path = self.board.get_card_image(7, 2)
        # image_path1 = self.board.get_card_image(6, 2)
        # image_path2 = self.board.get_card_image(6, 3)
        # print(image_path)
        # print(image_path1)
        # print(image_path2)

        # show the window

        # # Handle initial moves for both players
        # console_ui.display_message("{}'s turn for the initial move".format(self.player1.name))
        # self.handle_initial_move(self.player1, self.player2)
        #
        # console_ui.display_message("{}'s turn for the initial move".format(self.player2.name))
        # self.handle_initial_move(self.player2, self.player1)
        #
        # # After initial moves, continue with regular game loop
        # self.is_first_move = False
        #
        # while not self.game_over:
        #     current_player = self.player1 if self.player1_turn else self.player2
        #     opponent = self.player2 if self.player1_turn else self.player1
        #
        #     console_ui.add_line_break()
        #
        #     console_ui.display_message("{}'s turn".format(current_player.name))
        #     self.display_current_card(current_player)
        #     console_ui.add_line_break()
        #
        #     self.handle_player_move(current_player, opponent)
        #
        #     if moves.check_winning_move(current_player.xPosition, current_player.yPosition):
        #         self.game_over = True
        #         console_ui.display_message('')
        #         console_ui.add_line_break()
        #         console_ui.display_message("{} wins!".format(current_player.name))
        #         console_ui.add_line_break()
        #
        #     self.player1_turn = not self.player1_turn
        #     self.board.display_board(self.player1.xPosition, self.player1.yPosition, self.player2.xPosition,
        #                              self.player2.yPosition)
        #
        #     # if not self.player1_turn:  # This means Player 2 just completed their turn
        #     self.turn += 1
        # console_ui.display_message('===== Game Ended =====')
