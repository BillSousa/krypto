import random
from krypto.build_deck import build_deck

def deal(
    rng: random.Random | None = None,
) -> tuple[int, list[int]]:
    """Deal one Krypto round: a target card and a 5-card hand.

    Parameters
    ----------
    rng : random.Random, optional
        A seeded random source for deterministic, repeatable deals
        (used by tests). If None, a fresh unseeded random.Random() is
        used.

    Returns
    -------
    tuple[int, list[int]]
        (target, hand) — the first card drawn as target, the next
        five as hand, in that drawn order. hand has length 5.

    Raises
    ------
    None
    """
    if rng is None:
        rng = random.Random()

    deck = build_deck()
    rng.shuffle(deck)

    target = deck[0]
    hand = deck[1:6]

    return target, hand
