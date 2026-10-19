```python
import pytest
from fractions import Fraction

from krypto.evaluate import evaluate

HAND = [3, 5, 2, 12, 21]


def test_empty_token_chain_is_invalid():
    assert evaluate([], HAND, 5) == (False, False, None)


def test_adjacent_operators_is_invalid():
    assert evaluate([0, "+", "+", 1], HAND, 8) == (False, False, None)


def test_two_cards_in_a_row_is_invalid():
    # Cards 3 and 5 must not be joined into the number 35.
    assert evaluate([0, 1], HAND, 35) == (False, False, None)


def test_leading_operator_is_invalid():
    assert evaluate(["-", 0, "+", 1], HAND, 2) == (False, False, None)


def test_operator_after_open_paren_is_invalid():
    tokens = ["(", "-", 0, "+", 1, ")"]
    assert evaluate(tokens, HAND, 2) == (False, False, None)


def test_unbalanced_parens_is_invalid():
    is_valid, is_win, value = evaluate(["(", 0, "+", 1], HAND, 8)
    assert is_valid is False
    assert is_win is False
    assert value is None


def test_trailing_operator_is_invalid():
    assert evaluate([0, "+"], HAND, 3) == (False, False, None)


def test_empty_parentheses_is_invalid():
    # eval("()") would otherwise return an empty tuple, not a number.
    assert evaluate(["(", ")"], HAND, 5) == (False, False, None)


def test_division_by_zero_is_invalid():
    hand = [3, 4, 4, 8, 12]
    tokens = [0, "/", "(", 1, "-", 2, ")"]
    assert evaluate(tokens, hand, 1) == (False, False, None)


def test_valid_expression_wrong_answer():
    is_valid, is_win, value = evaluate([0, "+", 1], HAND, 9)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(8)


def test_valid_expression_correct_answer_is_win():
    is_valid, is_win, value = evaluate([0, "+", 1], HAND, 8)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(8)


def test_parens_and_precedence():
    tokens = ["(", 0, "+", 1, ")", "*", 2]
    is_valid, is_win, value = evaluate(tokens, HAND, 16)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(16)


def test_exact_fraction_arithmetic_no_float_error():
    # 1/3 * 3 must equal exactly 1 with Fraction, unlike float math.
    hand = [1, 3, 3, 8, 12]
    is_valid, is_win, value = evaluate([0, "/", 1, "*", 2], hand, 1)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(1)


def test_fractional_result_not_matching_target():
    hand = [1, 3, 5, 8, 12]
    is_valid, is_win, value = evaluate([0, "/", 1], hand, 1)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(1, 3)


def test_negative_intermediate_result_not_matching_target():
    is_valid, is_win, value = evaluate([0, "-", 1], HAND, 2)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(-2)


def test_single_card_can_win():
    is_valid, is_win, value = evaluate([1], HAND, 5)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(5)


def test_max_depth_parens():
    hand = [1, 2, 3, 4, 5]
    tokens = ["(", "(", "(", 0, "+", 1, ")", "*", 2, ")", "-", 3, ")", "+", 4]
    is_valid, is_win, value = evaluate(tokens, hand, 10)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(10)


def test_index_outside_hand_raises_index_error():
    # A bad index is a bug in the caller, so it is deliberately not caught.
    with pytest.raises(IndexError):
        evaluate([9], HAND, 1)
```