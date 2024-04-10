from core.enums.card_face import CardFace
from core.enums.card_suit import CardSuit
from core.enums.card_type import CardType
from core.enums.symbols import Symbols


class Board:
    def __init__(self, pack):
        # Initialize the board with a pack of cards
        self.card_list = pack.get_pack()
        # Set up the board with cards
        self.card_position = self.initialize_board()

    def initialize_board(self):
        # Create a 8x8 board and populate it with cards from the pack
        board = [[None for _ in range(8)] for _ in range(8)]
        index = 0
        for i in range(1, 8):
            for j in range(1, 8):
                # Skip the player starting positions
                if (i, j) not in [(1, 7), (7, 1)]:
                    board[i][j] = self.card_list[index]
                    index += 1
        return board

    def display_board(self, p1x, p1y, p2x, p2y):
        # Display the board, showing column headers and each row
        self.print_column_headers()
        for i in range(1, 8):
            self.print_row(i, p1x, p1y, p2x, p2y)
            print()  # Add a space after each row

    @staticmethod
    def print_column_headers():
        # Print the column numbers at the top of the board
        print(" ".join([f"{i:^12} " for i in range(1, 8)]))

    def print_row(self, row_num, p1x, p1y, p2x, p2y):
        # Print each row of the board with the row number and cell contents
        row = [f"{row_num:<2}"]
        for j in range(1, 8):
            cell_content = self.get_cell_content(row_num, j, p1x, p1y, p2x, p2y)
            row.append(f"{cell_content:^12}")
        print(" ".join(row))

    def get_cell_content(self, i, j, p1x, p1y, p2x, p2y):
        # Get the content of a cell, formatted based on the cell's purpose
        # the white (red) queen is in the bottom left corner which is i = 1 and j = 7
        if i == 1 and j == 7:
            red_queen = Symbols.RED_QUEEN.value
            return self.format_position(p1x, p1y, p2x, p2y, i, j, f"r.{red_queen}")

        # the black (spade) queen is in the bottom left corner which is i = 7 and j = 1
        elif i == 7 and j == 1:
            black_queen = Symbols.BLACK_QUEEN.value
            return self.format_position(p1x, p1y, p2x, p2y, i, j, f"b.{black_queen}")
        else:
            return self.format_regular_cell(i, j, p1x, p1y, p2x, p2y)

    @staticmethod
    def format_position(p1x, p1y, p2x, p2y, i, j, symbol):
        # Format a specific cell position based on player locations and the symbol
        if (p1x, p1y) == (i, j):
            black_king = Symbols.BLACK_KING.value
            return f"({black_king}) |{symbol}|"
        elif (p2x, p2y) == (i, j):
            red_king = Symbols.RED_KING.value
            return f"({red_king}) |{symbol}|"
        else:
            return f"|{symbol}|"

    def format_regular_cell(self, i, j, p1x, p1y, p2x, p2y):
        # Format a regular cell with a card or a player symbol
        piece = "\u2654" if (p1x, p1y) == (i, j) else "\u265A" if (p2x, p2y) == (i, j) else " "
        card = self.card_position[i][j]

        return f"{piece}{card}" if card else " "

    def get_card_string(self, x, y):
        # Return the string representation of the card at a specified position
        return str(self.card_position[x][y])

    # def get_card_image(self, x, y):
    #     # Get the card object at the specified position
    #     card_obj = self.card_position[x][y]
    #     print(card_obj)
    #
    #     # if card_obj:
    #     #     card_type = card_obj.card_type.name
    #     #     card_suit = card_obj.suit.name.lower()
    #     #     card_face = card_obj.face.name
    #     #
    #     #     # Handling numeral cards separately as they don't have 'type' in their name
    #     #     if card_type == 'RED_NUMERAL' or card_type == 'BLACK_NUMERAL':
    #     #         card_name = f"{card_face.lower()}_of_{card_suit}.png"
    #     #     # Handling face cards
    #     #     elif card_type in ['KING', 'QUEEN', 'JACK']:
    #     #         card_name = f"{card_type.lower()}_of_{card_suit}.png"
    #     #     # Handling ace cards
    #     #     elif card_face == 'ACE':
    #     #         card_name = f"ace_of_{card_suit}.png"
    #     #     # Handling joker cards
    #     #     elif card_type == 'JOKER':
    #     #         if card_suit == 'hearts' or card_suit == 'diamonds':
    #     #             color = 'red'
    #     #         else:
    #     #             color = 'black'
    #     #         card_name = f"{color}_joker.png"
    #     #     else:
    #     #         return "No matching card image found"
    #     #
    #     #     # Assuming all images are stored in a directory named 'card_images' within the resources folder
    #     #     path = f"resources/card_images/{card_name}"
    #     #     return path
    #     # else:
    #     #     return "No card at this position"

    # def get_card_image(self, x, y):
    #     # Get the card object at the specified position
    #     card_obj = self.card_position[x][y]
    #     if card_obj:
    #         # Extract the face and suit of the card
    #         card_face = card_obj.face
    #         card_suit = card_obj.suit

    #         # Determine the file name based on the card object attributes
    #         if card_obj.card_type == CardType.JOKER:
    #             # Assuming 'red_joker.png' or 'black_joker.png' for the joker cards
    #             color = 'red' if card_suit in [CardSuit.HEARTS, CardSuit.DIAMONDS] else 'black'
    #             card_name = f"{color}_joker.png"
    #         elif card_face == CardFace.KING:
    #             card_name = f"king_of_{card_suit.name.lower()}.png"
    #         elif card_face == CardFace.JACK:
    #             card_name = f"jack_of_{card_suit.name.lower()}.png"
    #         else:
    #             # Assuming numeral cards follow 'number_of_suit.png' format
    #             card_name = f"{card_face.value}_of_{card_suit.name.lower()}.png"

    #         # Assuming all images are stored in a directory named 'card_images' within the resources folder
    #         path = f"resources/card_images/{card_name}"
    #         return path
    #     else:
    #         return "No card at this position"

    def get_card_image(self, x, y):
        # Get the card object at the specified position
        card_obj = self.card_position[x][y]
        if card_obj:
            # Extract the face and suit of the card
            card_face = card_obj.face
            card_suit = card_obj.suit

            #   Determine the file name based on the card object attributes
            if card_obj.card_type == CardType.JOKER:
                # Assuming 'red_joker.png' or 'black_joker.png' for the joker cards
                color = 'red' if card_suit in [CardSuit.HEARTS, CardSuit.DIAMONDS] else 'black'
                card_name = f"{color}_joker.png"
            elif card_face == CardFace.KING:
                card_name = f"king_of_{card_suit.name.lower()}.png"
            elif card_face == CardFace.JACK:
                card_name = f"jack_of_{card_suit.name.lower()}.png"
            elif card_face == CardFace.ACE:
                # Handle the ace cards
                card_name = f"ace_of_{card_suit.name.lower()}.png"
            else:
                # Assuming numeral cards follow 'number_of_suit.png' format
                card_name = f"{card_face.value}_of_{card_suit.name.lower()}.png"

            # Assuming all images are stored in a directory named 'card_images' within the resources folder
            path = f"resources/card_images/{card_name}"
            return path
        else:
            return "No card at this position"
