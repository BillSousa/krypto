## Product Specification
N/A

## Implemenation
`deal.py` holds a single function, `deal(rng: random.Random | None =
None) -> tuple[int, list[int]]`, and it's the only place a round's
cards get chosen. First, it imports `build_deck` from `build_deck.py`.
Second, it shuffles a fresh copy of the 56-card list provided by 
`build_deck`. Shuffling uses `rng` if it is passed, so tests can pass 
a seeded `random.Random` for repeatable deals. If `rng` is not passed, 
which is the case in normal game-play, then an unseeded `random.Random` 
is used. Third, six cards are drawn from the shuffled deck. The first 
card drawn as `target`, the next five as `hand`, in that drawn order.
`target` is a plain `int`; `hand` is a `list[int]` of length 5, in
dealt order. There is no dedicated `Card` class — cards have no 
identity beyond their position in the hand list, so a plain `int` 
addressed by index is sufficient. Finally, `(target, hand)` is returned.
```python
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
```
