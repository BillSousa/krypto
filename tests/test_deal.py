import random

from krypto.build_deck import build_deck
from krypto.deal import deal


def test_deal_returns_target_and_hand_of_length_5():
    target, hand = deal(rng=random.Random(42))
    assert isinstance(target, int)
    assert isinstance(hand, list)
    assert len(hand) == 5


def test_deal_values_are_valid_card_values():
    target, hand = deal(rng=random.Random(42))
    assert 1 <= target <= 25
    assert all(1 <= card <= 25 for card in hand)


def test_deal_is_deterministic_with_same_seed():
    target_a, hand_a = deal(rng=random.Random(7))
    target_b, hand_b = deal(rng=random.Random(7))
    assert target_a == target_b
    assert hand_a == hand_b


def test_deal_matches_manual_shuffle_with_same_seed():
    deck = build_deck()
    random.Random(99).shuffle(deck)
    expected_target = deck[0]
    expected_hand = deck[1:6]

    target, hand = deal(rng=random.Random(99))

    assert target == expected_target
    assert hand == expected_hand


def test_deal_without_rng_does_not_raise():
    target, hand = deal()
    assert isinstance(target, int)
    assert len(hand) == 5


def test_deal_different_seeds_can_differ():
    target_a, hand_a = deal(rng=random.Random(1))
    target_b, hand_b = deal(rng=random.Random(2))
    assert (target_a, hand_a) != (target_b, hand_b)
