from collections import Counter

from krypto.build_deck import build_deck


def test_deck_has_56_cards():
    assert len(build_deck()) == 56


def test_deck_composition_matches_spec():
    counts = Counter(build_deck())
    expected = {}
    for value in range(1, 7):
        expected[value] = 3
    for value in range(7, 11):
        expected[value] = 4
    for value in range(11, 18):
        expected[value] = 2
    for value in range(18, 26):
        expected[value] = 1
    assert counts == expected


def test_deck_is_ascending():
    deck = build_deck()
    assert deck == sorted(deck)


def test_deck_values_in_range_1_to_25():
    deck = build_deck()
    assert all(1 <= value <= 25 for value in deck)


def test_deck_is_not_shuffled_each_call():
    assert build_deck() == build_deck()


def test_deck_calls_return_independent_lists():
    deck_a = build_deck()
    deck_b = build_deck()
    deck_a.append(99)
    assert 99 not in deck_b
