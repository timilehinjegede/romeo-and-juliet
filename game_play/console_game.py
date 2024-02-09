from core.classes.game_setup.board import Board
from core.classes.game_setup.pack import Pack
from core.classes.game_setup.player import Player
from core.classes.moves import moves
from interface.console import console_ui


class ConsoleGame:

    # def __init__(self):
    @staticmethod
    def request_players_info():
        # welcome both players to the romeo and juliet game
        console_ui.game_welcome()

        # ask for the players to enter their names
        player1_name = console_ui.ask_for_player_name(1)
        player2_name = console_ui.ask_for_player_name(2)

        # create the players
        player1 = Player(player1_name, 1)
        player2 = Player(player2_name, 2)

        console_ui.add_line_break()

        # welcome the players
        console_ui.welcome_players(player1_name, player2_name)
        pass

    # def arrange_cards(self):
    #     pass

    # def check_move(self, player, card):
    #     # Validate player's move
    #     pass

    # def make_move(self, player, card):
    #     # Validate player's move
    #     pass

    @staticmethod
    def play():
        p1_play = True
        game_over = False
        valid_move = False
        is_joker = False
        swap_x, swap_y = 0, 0  # Initialize swap coordinates
        turn = 1

        # welcome both players to the romeo and juliet game
        console_ui.game_welcome()

        # ask for the players to enter their names
        player1_name = console_ui.ask_for_player_name(1)
        player2_name = console_ui.ask_for_player_name(2)

        # create the players
        player1 = Player(player1_name, 1)
        player2 = Player(player2_name, 2)

        console_ui.add_line_break()

        # welcome the players
        console_ui.welcome_players(player1_name, player2_name)

        # create the pack of cards to be used for the gameplay
        console_ui.display_message('Creating the game...')
        # create the packs of card to be used
        card_pack = Pack()

        # display a message to the users that the game is being setup
        console_ui.display_message('Shuffling the pack...')
        # shuffle the card pack
        card_pack.shuffle_pack()

        # display a message to the users that the game is being setup
        console_ui.display_message('Arranging the cards...')
        # create the board for the game
        board = Board(card_pack)

        console_ui.add_line_break()

        # display the initial board
        board.display_board(player1.xPosition, player1.yPosition, player2.xPosition, player2.yPosition)

        # player moves

        # check player move
        p1_x = player1.xPosition
        p1_y = player1.yPosition
        p2_x = player2.xPosition
        p2_y = player2.yPosition

        # rinse and repeat
        while not game_over:
            if turn == 1:
                if p1_play:
                    print("\n<Move {}>".format(turn))
                    while not valid_move:
                        x = int(input("X: "))
                        y = int(input("Y: "))
                        is_valid_move = moves.king_move(player1.xPosition, player1.yPosition, x, y)

                        if is_valid_move:
                            p1_x, p1_y = x, y
                            print("\nValid move!\n{}'s new position: [{}][{}]".format(player1.name, p1_x, p1_y))
                            valid_move = True
                        else:
                            print("Invalid move, try again!")

                    p1_play = not p1_play

                    board.display_board(p1_x, p1_y, p2_x, p2_y)

                if not p1_play:
                    print("\n<Move {}>".format(turn))
                    while not valid_move:
                        x = int(input("X: "))
                        y = int(input("Y: "))
                        is_valid_move = moves.king_move(player2.xPosition, player2.yPosition, x, y)

                        if is_valid_move:
                            p2_x, p2_y = x, y
                            print("\nValid move!\n{}'s new position: [{}][{}]".format(player2.name, p2_x, p2_y))
                            valid_move = True
                        else:
                            print("Invalid move, try again!")

                    p1_play = not p1_play

                turn += 1
                board.display_board(p1_x, p1_y, p2_x, p2_y)
        else:
            if p1_play:
                print("\n<Move {}>".format(turn))
                choice = console_ui.turn_choice()

                if choice == 1:
                    card = board.get_card_string(p1_x, p1_y)

                    if "JOKER" in card:
                        while not valid_move:
                            x = int(input("X: "))
                            y = int(input("Y: "))

                            if not moves.check_move(x, y, p2_x, p2_y, 1):
                                print("Invalid move, try again!")
                            elif moves.joker_move(p1_x, p1_y, x, y):
                                p1_x, p1_y = x, y
                                print("\nValid move!\n{}'s new position: [{}][{}]".format(player1.name, p1_x, p1_y))
                                valid_move = True
                            else:
                                print("Invalid move, try again!")

                    elif "K" in card:
                        while not valid_move:
                            x = int(input("X: "))
                            y = int(input("Y: "))

                            if not moves.check_move(x, y, p2_x, p2_y, 1):
                                print("Invalid move, try again!")
                            elif moves.king_move(p1_x, p1_y, x, y):
                                p1_x, p1_y = x, y
                                print("\nValid move!\n{}'s new position: [{}][{}]".format(player1.name, p1_x, p1_y))
                                valid_move = True
                            else:
                                print("Invalid move, try again!")

                    # Handle other card types similarly

                    p1_play = not p1_play

                if choice == 2:
                    joker_x, joker_y = 0, 0
                    print("\nEnter JOKER position..")

                    while not is_joker:
                        joker_x = int(input("X: "))
                        joker_y = int(input("Y: "))

                        card = board.get_card_string(joker_x, joker_y)

                        if "JOKER" in card:
                            is_joker = True
                        else:
                            print("Card is not a JOKER card, try again!")

                    print("\nEnter card position..")

                    while not valid_move:
                        x = int(input("X: "))
                        y = int(input("Y: "))

                        if swap_x == x and swap_y == y:
                            print("Cannot perform swap on the same card again! Please select another card to swap..")
                        elif "JOKER" in board.get_card_string(x, y):
                            print("Cannot perform swap of joker with joker! Please select another card to swap..")
                        elif (x == p2_x and y == p2_y) or (joker_x == p2_x and joker_y == p2_y) \
                                or (x == p1_x and y == p1_y) or (joker_x == p1_x and joker_y == p1_y):
                            print("Cannot perform swap on card occupied by self or the opponent! "
                                  "Please select another card to swap..")
                        elif moves.check_swap(x, y, joker_x, joker_y):
                            board.card_list[joker_x][joker_y], board.card_list[x][y] = board.card_list[x][y], "JOKER"
                            print(
                                "\nValid swap!\nJOKER swapped from [{}][{}] to [{}][{}]".format(joker_x, joker_y, x, y))
                            swap_x, swap_y = joker_x, joker_y
                            valid_move = True
                        else:
                            print("Invalid swap, try again!")

                    p1_play = not p1_play

            # Handle player 2 moves similarly

            if moves.check_winning_move(p1_x, p1_y):
                game_over = True
                print("{} wins!".format(player1.name))
                board.display_board(p1_x, p1_y, p2_x, p2_y)
                return

            board.display_board(p1_x, p1_y, p2_x, p2_y)

            if not p1_play:
                # Handle player 2 moves similarly
                pass

            if moves.check_winning_move(p2_x, p2_y) == 1:
                game_over = True
                print("{} wins!".format(player2.name))
                board.display_board(p1_x, p1_y, p2_x, p2_y)
                return

            turn += 1
            board.display_board(p1_x, p1_y, p2_x, p2_y)

    # after a winner has been deptermined
    # play_again = input("Play again? (Y/N)").strip().upper()

    # if play_again == 'Y':
    #     play()
    # else:
    #     exit()
