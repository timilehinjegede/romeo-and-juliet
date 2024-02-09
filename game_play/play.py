import time

def play(is_ai):
    p1_play = True
    valid_move = False
    is_joker = False
    game_over = False
    turn = 1

    swap_x, swap_y = 0, 0  # Initialize swap coordinates

    while not game_over:
        if turn == 1:
            if p1_play:
                print("\n<Move {}>".format(turn))
                while not valid_move:
                    x = int(input("X: "))
                    y = int(input("Y: "))
                    king_move = check_move(p1_x, p1_y, x, y)

                    if king_move == 1:
                        p1_x, p1_y = x, y
                        print("\nValid move!\n{}'s new position: [{}][{}]".format(p1_name, p1_x, p1_y))
                        valid_move = True
                    else:
                        print("Invalid move, try again!")

                p1_play = not p1_play

            display_board(p1_x, p1_y, p2_x, p2_y)

            if not p1_play:
                print("\n<Move {}>".format(turn))
                if is_ai:
                    ai_play = AIPlay(board, p1_x, p1_y, p2_x, p2_y, True)
                    ai_play.best_move()
                    p2_x, p2_y = ai_play.get_best_x(), ai_play.get_best_y()
                    time.sleep(1)
                    print("\n{}'s new position: [{}][{}]".format(p2_name, p2_x, p2_y))
                    valid_move = True
                else:
                    while not valid_move:
                        x = int(input("X: "))
                        y = int(input("Y: "))
                        king_move = check_move(p2_x, p2_y, x, y)

                        if king_move == 1:
                            p2_x, p2_y = x, y
                            print("\nValid move!\n{}'s new position: [{}][{}]".format(p2_name, p2_x, p2_y))
                            valid_move = True
                        else:
                            print("Invalid move, try again!")

                p1_play = not p1_play

            turn += 1
            display_board(p1_x, p1_y, p2_x, p2_y)
        else:
            if p1_play:
                print("\n<Move {}>".format(turn))
                choice = move_choice()

                if choice == 1:
                    card = get_card_string(p1_x, p1_y)

                    if "JOKER" in card:
                        while not valid_move:
                            x = int(input("X: "))
                            y = int(input("Y: "))
                            joker_move = JokerMove()

                            if not validate_move(x, y, p2_x, p2_y, 1):
                                print("Invalid move, try again!")
                            elif joker_move.check_move(p1_x, p1_y, x, y) == 1:
                                p1_x, p1_y = x, y
                                print("\nValid move!\n{}'s new position: [{}][{}]".format(p1_name, p1_x, p1_y))
                                valid_move = True
                            else:
                                print("Invalid move, try again!")

                    elif "K" in card:
                        while not valid_move:
                            x = int(input("X: "))
                            y = int(input("Y: "))
                            king_move = KingMove()

                            if not validate_move(x, y, p2_x, p2_y, 1):
                                print("Invalid move, try again!")
                            elif king_move.check_move(p1_x, p1_y, x, y) == 1:
                                p1_x, p1_y = x, y
                                print("\nValid move!\n{}'s new position: [{}][{}]".format(p1_name, p1_x, p1_y))
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

                        card = get_card_string(joker_x, joker_y)

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
                        elif "JOKER" in get_card_string(x, y):
                            print("Cannot perform swap of joker with joker! Please select another card to swap..")
                        elif (x == p2_x and y == p2_y) or (joker_x == p2_x and joker_y == p2_y) \
                                or (x == p1_x and y == p1_y) or (joker_x == p1_x and joker_y == p1_y):
                            print("Cannot perform swap on card occupied by self or the opponent! "
                                  "Please select another card to swap..")
                        elif check_swap(x, y, joker_x, joker_y) == 1:
                            board[joker_x][joker_y], board[x][y] = board[x][y], "JOKER"
                            print("\nValid swap!\nJOKER swapped from [{}][{}] to [{}][{}]".format(joker_x, joker_y, x, y))
                            swap_x, swap_y = joker_x, joker_y
                            valid_move = True
                        else:
                            print("Invalid swap, try again!")

                    p1_play = not p1_play

            # Handle player 2 moves similarly

            if check_winning_move(p1_x, p1_y) == 1:
                game_over = True
                print("{} wins!".format(p1_name))
                display_board(p1_x, p1_y, p2_x, p2_y)
                break

            display_board(p1_x, p1_y, p2_x, p2_y)

            if not p1_play:
                # Handle player 2 moves similarly
                pass

            if check_winning_move(p2_x, p2_y) == 1:
                game_over = True
                print("{} wins!".format(p2_name))
                display_board(p1_x, p1_y, p2_x, p2_y)
                break

            turn += 1
            display_board(p1_x, p1_y, p2_x, p2_y)

    play_again = input("Play again? (Y/N)").strip().upper()

    if play_again == 'Y':
        main_menu()
    else:
        exit()



while not game_over:
    if turn == 1:
        if p1_play:
            print("\n<Move {}>".format(turn))
            while not valid_move:
                x = int(input("X: "))
                y = int(input("Y: "))
                king_move = check_move(p1_x, p1_y, x, y)

                if king_move == 1:
                    p1_x, p1_y = x, y
                    print("\nValid move!\n{}'s new position: [{}][{}]".format(p1_name, p1_x, p1_y))
                    valid_move = True
                else:
                    print("Invalid move, try again!")

            p1_play = not p1_play

        display_board(p1_x, p1_y, p2_x, p2_y)

        if not p1_play:
            print("\n<Move {}>".format(turn))
            while not valid_move:
                x = int(input("X: "))
                y = int(input("Y: "))
                king_move = check_move(p2_x, p2_y, x, y)

                if king_move == 1:
                    p2_x, p2_y = x, y
                    print("\nValid move!\n{}'s new position: [{}][{}]".format(p2_name, p2_x, p2_y))
                    valid_move = True
                else:
                    print("Invalid move, try again!")

            p1_play = not p1_play

        turn += 1
        display_board(p1_x, p1_y, p2_x, p2_y)
    else:
        if p1_play:
            print("\n<Move {}>".format(turn))
            choice = move_choice()

            if choice == 1:
                card = get_card_string(p1_x, p1_y)

                if "JOKER" in card:
                    while not valid_move:
                        x = int(input("X: "))
                        y = int(input("Y: "))
                        joker_move = JokerMove()

                        if not validate_move(x, y, p2_x, p2_y, 1):
                            print("Invalid move, try again!")
                        elif joker_move.check_move(p1_x, p1_y, x, y) == 1:
                            p1_x, p1_y = x, y
                            print("\nValid move!\n{}'s new position: [{}][{}]".format(p1_name, p1_x, p1_y))
                            valid_move = True
                        else:
                            print("Invalid move, try again!")

                elif "K" in card:
                    while not valid_move:
                        x = int(input("X: "))
                        y = int(input("Y: "))
                        king_move = KingMove()

                        if not validate_move(x, y, p2_x, p2_y, 1):
                            print("Invalid move, try again!")
                        elif king_move.check_move(p1_x, p1_y, x, y) == 1:
                            p1_x, p1_y = x, y
                            print("\nValid move!\n{}'s new position: [{}][{}]".format(p1_name, p1_x, p1_y))
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

                    card = get_card_string(joker_x, joker_y)

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
                    elif "JOKER" in get_card_string(x, y):
                        print("Cannot perform swap of joker with joker! Please select another card to swap..")
                    elif (x == p2_x and y == p2_y) or (joker_x == p2_x and joker_y == p2_y) \
                            or (x == p1_x and y == p1_y) or (joker_x == p1_x and joker_y == p1_y):
                        print("Cannot perform swap on card occupied by self or the opponent! "
                              "Please select another card to swap..")
                    elif check_swap(x, y, joker_x, joker_y) == 1:
                        board[joker_x][joker_y], board[x][y] = board[x][y], "JOKER"
                        print("\nValid swap!\nJOKER swapped from [{}][{}] to [{}][{}]".format(joker_x, joker_y, x, y))
                        swap_x, swap_y = joker_x, joker_y
                        valid_move = True
                    else:
                        print("Invalid swap, try again!")

                p1_play = not p1_play

        # Handle player 2 moves similarly

        if check_winning_move(p1_x, p1_y) == 1:
            game_over = True
            print("{} wins!".format(p1_name))
            display_board(p1_x, p1_y, p2_x, p2_y)
            break

        display_board(p1_x, p1_y, p2_x, p2_y)

        if not p1_play:
            # Handle player 2 moves similarly
            pass

        if check_winning_move(p2_x, p2_y) == 1:
            game_over = True
            print("{} wins!".format(p2_name))
            display_board(p1_x, p1_y, p2_x, p2_y)
            break

        turn += 1
        display_board(p1_x, p1_y, p2_x, p2_y)
