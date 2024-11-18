
SUITS = ["s", "c", "h", "d"]
CARDS = "AKQJT98765432"

HAND_RANKINGS = ("High Card", "Pair", "Two Pair", "Three of a Kind",
                 "Straight", "Flush", "Full House", "Four of a Kind",
                 "Straight Flush", "Royal Flush")

CARD_VALUES = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
for card in range(2, 10):
    CARD_VALUES[str(card)] = card

BOARD_LOWER_COLOR = (0, 60, 0)   # Lower main board color range
BOARD_HIGHER_COLOR = (20, 110, 30)  # Upper main board color range