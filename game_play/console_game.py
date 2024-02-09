from core.classes.game_setup.board import Board
from core.classes.game_setup.pack import Pack
from core.classes.game_setup.player import Player
from core.classes.moves import moves
from core.enums.direction import Direction
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
        player1_turn = True
        game_over = False
        valid_move = False
        is_joker = False
        turn = 1
        is_first_move = True

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

        # rinse and repeat
        while not game_over:
            if is_first_move:
                if player1_turn:
                    print("\n<Move {}>".format(turn))
                    valid_move = False
                    while not valid_move:
                        x = int(input("X: "))
                        y = int(input("Y: "))
                        is_valid_move = moves.king_move(player1.xPosition, player1.yPosition, x, y)

                        if is_valid_move:
                            player1.set_position(x, y)
                            # p1_x, p1_y = x, y
                            print("\nValid move!\n{}'s new position: [{}][{}]".format(player1.name, player1.xPosition,
                                                                                      player1.yPosition))
                            valid_move = True
                        else:
                            print("Invalid move, try again!")
                            valid_move = False

                    player1_turn = not player1_turn

                board.display_board(player1.xPosition, player1.yPosition, player2.xPosition, player2.yPosition)

                if not player1_turn:
                    print("\n<Move {}>".format(turn))
                    valid_move = False
                    while not valid_move:
                        x = int(input("X: "))
                        y = int(input("Y: "))
                        is_valid_move = moves.king_move(player2.xPosition, player2.yPosition, x, y)

                        if is_valid_move:
                            # p2_x, p2_y = x, y
                            player2.set_position(x, y)
                            print("\nValid move!\n{}'s new position: [{}][{}]".format(player2.name, player2.xPosition,
                                                                                      player2.yPosition))
                            valid_move = True
                        else:
                            print("Invalid move, try again!")
                            valid_move = False

                    player1_turn = not player1_turn

                turn += 1
                is_first_move = False
                board.display_board(player1.xPosition, player1.yPosition, player2.xPosition, player2.yPosition)

            else:
                if player1_turn:
                    print("\n<Move {}>".format(turn))
                    choice = console_ui.turn_choice()

                    # move conditions
                    if choice == 1:
                        card = board.get_card_string(player1.xPosition, player1.yPosition)

                        # joker move
                        if "JOKER" in card:
                            valid_move = False

                            while not valid_move:
                                x = int(input("X: "))
                                y = int(input("Y: "))

                                if not moves.check_move(x, y, player2.xPosition, player2.yPosition, 1):
                                    print("Invalid move, try again!")
                                    valid_move = False

                                elif moves.joker_move(player1.xPosition, player1.yPosition, x, y):
                                    # p1_x, p1_y = x, y
                                    player1.set_position(x, y)
                                    print("\nValid move!\n{}'s new position: [{}][{}]".format(player1.name,
                                                                                              player1.xPosition,
                                                                                              player1.yPosition))
                                    valid_move = True
                                else:
                                    print("Invalid move, try again!")
                                    valid_move = False

                        # king move
                        elif "K" in card:
                            valid_move = False

                            while not valid_move:
                                x = int(input("X: "))
                                y = int(input("Y: "))

                                if not moves.check_move(x, y, player2.xPosition, player2.yPosition, 1):
                                    print("Invalid move, try again!")
                                    valid_move = False

                                elif moves.king_move(player1.xPosition, player1.yPosition, x, y):
                                    # p1_x, p1_y = x, y
                                    player1.set_position(x, y)
                                    print("\nValid move!\n{}'s new position: [{}][{}]".format(player1.name,
                                                                                              player1.xPosition,
                                                                                              player1.yPosition))
                                    valid_move = True
                                else:
                                    print("Invalid move, try again!")
                                    valid_move = False

                        # Jack move
                        elif "J" in card:
                            valid_move = False

                            while not valid_move:
                                x = int(input("X: "))
                                y = int(input("Y: "))

                                if not moves.check_move(x, y, player2.xPosition, player2.yPosition, 1):
                                    print("Invalid move, try again!")
                                    valid_move = False
                                elif moves.knight_move(player1.xPosition, player1.yPosition, x, y):
                                    # p1_x, p1_y = x, y
                                    player1.set_position(x, y)
                                    print("\nValid move!\n{}'s new position: [{}][{}]".format(player1.name,
                                                                                              player1.xPosition,
                                                                                              player1.yPosition))
                                    valid_move = True
                                else:
                                    print("Invalid move, try again!")
                                    valid_move = False

                        # black numeral card => SPADES OR CLUBS
                        elif "\u2660" in card or "\u2663" in card:
                            valid_move = False

                            while not valid_move:
                                card_face = board.get_card_string(player1.xPosition, player1.yPosition)
                                move_count = int(card_face[1:3].strip())

                                # Ask player for the direction of the move (Right or Left)
                                print(f"\nMove {move_count} steps, right or left (R/L): ")
                                rl = input()
                                direction = Direction.RIGHT if rl == 'R' else Direction.LEFT

                                y = moves.y_position_count(player1.yPosition, move_count, direction)

                                if not moves.check_move(player1.xPosition, y, player2.xPosition,
                                                        player2.yPosition, 1):
                                    print("Invalid move, try again!")
                                    valid_move = False
                                else:
                                    if y == 0:
                                        print("Invalid move, try again!")
                                        valid_move = False
                                    else:
                                        player1.set_position(player1.xPosition, y)
                                        # p1_x, p1_y = x, y
                                        #     player1.set_position(x, y)
                                        print("\nValid move!\n{}'s new position: [{}][{}]".format(player1.name,
                                                                                                  player1.xPosition,
                                                                                                  player1.yPosition))
                                        valid_move = True

                        # red numeral card (in this case - WHITE) => HEARTS OR DIAMONDS
                        elif "\u2661" in card or "\u2662" in card:
                            valid_move = False

                            while not valid_move:
                                card_face = board.get_card_string(player1.xPosition, player1.yPosition)
                                move_count = int(card_face[1:3].strip())

                                # Ask player for the direction of the move (Up or Down)
                                print(f"\nMove {move_count} steps, up or down (U/D): ")
                                rl = input()
                                direction = Direction.UP if rl == 'U' else Direction.DOWN

                                x = moves.x_position_count(player1.xPosition, move_count, direction)

                                if not moves.check_move(x, player1.yPosition, player2.xPosition,
                                                        player2.yPosition, 1):
                                    print("Invalid move, try again!")
                                    valid_move = False
                                else:
                                    if x == 0:
                                        print("Invalid move, try again!")
                                        valid_move = False
                                    else:
                                        player1.set_position(x, player1.yPosition)
                                        # p1_x, p1_y = x, y
                                        #     player1.set_position(x, player1.yPosition)
                                        print("\nValid move!\n{}'s new position: [{}][{}]".format(player1.name,
                                                                                                  player1.xPosition,
                                                                                                  player1.yPosition))
                                        valid_move = True

                        # default if no match is found
                        else:
                            break

                    # card swap condition
                    if choice == 2:
                        joker_x, joker_y = 0, 0
                        print("\nEnter JOKER position..")
                        is_joker = False

                        while not is_joker:
                            joker_x = int(input("X: "))
                            joker_y = int(input("Y: "))

                            # handle list out of range
                            card = board.get_card_string(joker_x, joker_y)

                            if "JOKER" in card:
                                is_joker = True
                            else:
                                print("Card is not a JOKER card, try again!")

                        print("\nEnter card position..")
                        valid_move = False

                        while not valid_move:
                            x = int(input("X: "))
                            y = int(input("Y: "))

                            if moves.last_x_swap() == x and moves.last_y_swap() == y:
                                print(
                                    "Cannot perform swap on the same card again! Please select another card to swap..")
                                valid_move = False

                            elif "JOKER" in board.get_card_string(x, y):
                                print("Cannot perform swap of joker with joker! Please select another card to swap..")
                                valid_move = False

                            elif (x == player2.xPosition and y == player2.yPosition) or (joker_x == player2.xPosition
                                                                                         and joker_y ==
                                                                                         player2.yPosition) \
                                    or (x == player1.xPosition and y == player1.yPosition) or (joker_x ==
                                                                                               player1.xPosition and
                                                                                               joker_y ==
                                                                                               player1.yPosition):
                                print("Cannot perform swap on card occupied by self or the opponent! "
                                      "Please select another card to swap..")
                                valid_move = False

                            elif moves.check_swap(x, y, joker_x, joker_y):
                                board.card_position[joker_x][joker_y], board.card_position[x][y] = (
                                    board.card_position[x][y], "JOKER")
                                print(
                                    "\nValid swap!\nJOKER swapped from [{}][{}] to [{}][{}]".format(joker_x, joker_y, x,
                                                                                                    y))
                                moves.save_swap(joker_x, joker_y)
                                valid_move = True
                            else:
                                print("Invalid swap, try again!")
                                valid_move = False

                    player1_turn = not player1_turn

            if moves.check_winning_move(player1.xPosition, player1.yPosition):
                game_over = True
                print("{} wins!".format(player1.name))
                board.display_board(player1.xPosition, player1.yPosition, player2.xPosition, player2.yPosition)
                break

            board.display_board(player1.xPosition, player1.yPosition, player2.xPosition, player2.yPosition)

            # Handle player 2 moves similarly
            if not player1_turn:
                print("\n<Move {}>".format(turn))
                choice = console_ui.turn_choice()

                # move conditions
                if choice == 1:
                    card = board.get_card_string(player2.xPosition, player2.yPosition)

                    # joker move
                    if "JOKER" in card:
                        valid_move = False

                        while not valid_move:
                            x = int(input("X: "))
                            y = int(input("Y: "))

                            if not moves.check_move(x, y, player1.xPosition, player1.yPosition, 2):
                                print("Invalid move, try again!")
                                valid_move = False

                            elif moves.joker_move(player2.xPosition, player2.yPosition, x, y):
                                # p1_x, p1_y = x, y
                                player2.set_position(x, y)
                                print("\nValid move!\n{}'s new position: [{}][{}]".format(player2.name,
                                                                                          player2.xPosition,
                                                                                          player2.yPosition))
                                valid_move = True
                            else:
                                print("Invalid move, try again!")
                                valid_move = False

                    # king move
                    elif "K" in card:
                        valid_move = False

                        while not valid_move:
                            x = int(input("X: "))
                            y = int(input("Y: "))

                            if not moves.check_move(x, y, player1.xPosition, player1.yPosition, 2):
                                print("Invalid move, try again!")
                                valid_move = False

                            elif moves.king_move(player2.xPosition, player2.yPosition, x, y):
                                # p1_x, p1_y = x, y
                                player2.set_position(x, y)
                                print("\nValid move!\n{}'s new position: [{}][{}]".format(player2.name,
                                                                                          player2.xPosition,
                                                                                          player2.yPosition))
                                valid_move = True
                            else:
                                print("Invalid move, try again!")
                                valid_move = False

                    # Jack move
                    elif "J" in card:
                        valid_move = False

                        while not valid_move:
                            x = int(input("X: "))
                            y = int(input("Y: "))

                            if not moves.check_move(x, y, player1.xPosition, player1.yPosition, 2):
                                print("Invalid move, try again!")
                                valid_move = False
                            elif moves.knight_move(player2.xPosition, player2.yPosition, x, y):
                                # p1_x, p1_y = x, y
                                player2.set_position(x, y)
                                print("\nValid move!\n{}'s new position: [{}][{}]".format(player2.name,
                                                                                          player2.xPosition,
                                                                                          player2.yPosition))
                                valid_move = True
                            else:
                                print("Invalid move, try again!")
                                valid_move = False

                    # black numeral card => SPADES OR CLUBS
                    elif "\u2660" in card or "\u2663" in card:
                        valid_move = False

                        while not valid_move:
                            card_face = board.get_card_string(player2.xPosition, player2.yPosition)
                            move_count = int(card_face[1:3].strip())

                            # Ask player for the direction of the move (Right or Left)
                            print(f"\nMove {move_count} steps, right or left (R/L): ")
                            rl = input()
                            direction = Direction.RIGHT if rl == 'R' else Direction.LEFT

                            y = moves.y_position_count(player2.yPosition, move_count, direction)

                            if not moves.check_move(player2.xPosition, y, player1.xPosition,
                                                    player1.yPosition, 2):
                                print("Invalid move, try again!")
                                valid_move = False
                            else:
                                if y == 0:
                                    print("Invalid move, try again!")
                                    valid_move = False
                                else:
                                    player2.set_position(player2.xPosition, y)
                                    # p1_x, p1_y = x, y
                                    #     player1.set_position(x, y)
                                    print("\nValid move!\n{}'s new position: [{}][{}]".format(player2.name,
                                                                                              player2.xPosition,
                                                                                              player2.yPosition))
                                    valid_move = True

                    # red numeral card (in this case - WHITE) => HEARTS OR DIAMONDS
                    elif "\u2661" in card or "\u2662" in card:
                        valid_move = False

                        while not valid_move:
                            card_face = board.get_card_string(player2.xPosition, player2.yPosition)
                            move_count = int(card_face[1:3].strip())

                            # Ask player for the direction of the move (Up or Down)
                            print(f"\nMove {move_count} steps, up or down (U/D): ")
                            rl = input()
                            direction = Direction.UP if rl == 'U' else Direction.DOWN

                            x = moves.x_position_count(player2.xPosition, move_count, direction)

                            if not moves.check_move(x, player2.yPosition, player1.xPosition,
                                                    player1.yPosition, 2):
                                print("Invalid move, try again!")
                                valid_move = False
                            else:
                                if x == 0:
                                    print("Invalid move, try again!")
                                    valid_move = False
                                else:
                                    player2.set_position(x, player1.yPosition)
                                    # p1_x, p1_y = x, y
                                    #     player1.set_position(x, player1.yPosition)
                                    print("\nValid move!\n{}'s new position: [{}][{}]".format(player2.name,
                                                                                              player2.xPosition,
                                                                                              player2.yPosition))
                                    valid_move = True

                    # default if no match is found
                    else:
                        break

                # card swap condition
                if choice == 2:
                    joker_x, joker_y = 0, 0
                    print("\nEnter JOKER position..")
                    is_joker = False

                    while not is_joker:
                        joker_x = int(input("X: "))
                        joker_y = int(input("Y: "))

                        # handle list out of range
                        card = board.get_card_string(joker_x, joker_y)

                        if "JOKER" in card:
                            is_joker = True
                        else:
                            print("Card is not a JOKER card, try again!")

                    print("\nEnter card position..")
                    valid_move = False

                    while not valid_move:
                        x = int(input("X: "))
                        y = int(input("Y: "))

                        if moves.last_x_swap() == x and moves.last_y_swap() == y:
                            print(
                                "Cannot perform swap on the same card again! Please select another card to swap..")
                            valid_move = False

                        elif "JOKER" in board.get_card_string(x, y):
                            print("Cannot perform swap of joker with joker! Please select another card to swap..")
                            valid_move = False

                        elif (x == player2.xPosition and y == player2.yPosition) or (joker_x == player2.xPosition
                                                                                     and joker_y ==
                                                                                     player2.yPosition) \
                                or (x == player1.xPosition and y == player1.yPosition) or (joker_x ==
                                                                                           player1.xPosition and
                                                                                           joker_y ==
                                                                                           player1.yPosition):
                            print("Cannot perform swap on card occupied by self or the opponent! "
                                  "Please select another card to swap..")
                            valid_move = False

                        elif moves.check_swap(x, y, joker_x, joker_y):
                            board.card_position[joker_x][joker_y], board.card_position[x][y] = (
                                board.card_position[x][y], "JOKER")
                            print(
                                "\nValid swap!\nJOKER swapped from [{}][{}] to [{}][{}]".format(joker_x, joker_y, x,
                                                                                                y))
                            moves.save_swap(joker_x, joker_y)
                            valid_move = True
                        else:
                            print("Invalid swap, try again!")
                            valid_move = False

                player1_turn = not player1_turn

            if moves.check_winning_move(player2.xPosition, player2.yPosition):
                game_over = True
                print("{} wins!".format(player2.name))
                board.display_board(player1.xPosition, player1.yPosition, player2.xPosition, player2.yPosition)
                break

            turn += 1
            board.display_board(player1.xPosition, player1.yPosition, player2.xPosition, player2.yPosition)

        # after a winner has been determined
        # if game_over:
        #     play_again = input("Play again? (Y/N)").strip().upper()
        #     if play_again == 'Y':
        #         play()
        #     else:
        #         exit()
