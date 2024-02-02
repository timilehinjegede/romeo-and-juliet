from core.enums.card_face import CardFace
from core.enums.card_type import CardType


class Card:
    def __init__(self, suit, face, card_type=None):
        self.suit = suit
        self.face = face
        self.card_type = card_type

    # def __repr__(self):
    #     card_type_str = self.card_type.name.title() if self.card_type else "None"
    #     return f"{self.face.name.title()} of {self.suit.name.title()} (Type: {card_type_str})"

    def __str__(self):
        if self.card_type == CardType.JOKER:
            return "[ JOKER ]"
        elif self.face == CardFace.KING:
            return f"[K {self.suit.value}]"
        elif self.face == CardFace.JACK:
            return f"[J {self.suit.value}]"
        else:
            return f"[{self.face.value} {self.suit.value}]"
