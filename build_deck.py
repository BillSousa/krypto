from typing import List

def build_deck() -> List[int]:
    """Build the standard 56-card Krypto deck.

    Returns
    -------
    List[int]
        A fresh 56-item list, unshuffled, in ascending order. Built
        from SPEC §3's exact counts: values 1-6 appear 3 times each,
        7-10 appear 4 times each, 11-17 appear 2 times each, and
        18-25 appear 1 time each.

    Raises
    ------
    None
    """
    deck: List[int] = []

    for value in range(1, 7):
        deck.extend([value] * 3)

    for value in range(7, 11):
        deck.extend([value] * 4)

    for value in range(11, 18):
        deck.extend([value] * 2)

    for value in range(18, 26):
        deck.extend([value] * 1)

    return deck
