import random

from core.classes.game_setup.card import Card
from core.enums.card_face import CardFace
from core.enums.card_suit import CardSuit
from core.enums.card_type import CardType


class Pack:
    def __init__(self):
        self.cards = []

        # Add the 44 cards to the pack
        for suit in CardSuit:
            for face in CardFace:
                card = Card(suit, face)
                self.cards.append(card)

        # Add 3 jokers to the pack
        for _ in range(3):
            card = Card(None, None, CardType.JOKER)
            self.cards.append(card)

        # Shuffle the cards
        random.shuffle(self.cards)

    def get_pack(self):
        return self.cards
