### build_deck.py
`build_deck.py` holds a single function, `build_deck() -> list[int]`,
and it's the only place the 56-card composition lives in code. It
takes no arguments and returns a fresh 56-item list, unshuffled, in
ascending order, built from the exact counts in SPEC §3 (1–6 three
times each, 7–10 four times each, 11–17 twice each, 18–25 once each) —
never a random or partial deck.
```python
def build_deck() -> list[int]:
    """Build the standard 56-card Krypto deck.

    Returns
    -------
    list[int]
        A fresh 56-item list, unshuffled, in ascending order. Built
        from SPEC §3's exact counts: values 1-6 appear 3 times each,
        7-10 appear 4 times each, 11-17 appear 2 times each, and
        18-25 appear 1 time each.

    Raises
    ------
    None
    """
    deck: list[int] = []

    for value in range(1, 7):
        deck.extend([value] * 3)

    for value in range(7, 11):
        deck.extend([value] * 4)

    for value in range(11, 18):
        deck.extend([value] * 2)

    for value in range(18, 26):
        deck.extend([value] * 1)

    return deck
```
