```python
from fractions import Fraction

from krypto.evaluate import evaluate


def test_empty_string_is_invalid():
    assert evaluate("", 5) == (False, False, None)


def test_adjacent_operators_is_invalid():
    assert evaluate("3++5", 8) == (False, False, None)


def test_unbalanced_parens_is_invalid():
    is_valid, is_win, value = evaluate("(3+5", 8)
    assert is_valid is False
    assert is_win is False
    assert value is None


def test_division_by_zero_is_invalid():
    is_valid, is_win, value = evaluate("3/0", 3)
    assert is_valid is False
    assert is_win is False
    assert value is None


def test_valid_expression_wrong_answer():
    is_valid, is_win, value = evaluate("3+5", 9)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(8)


def test_valid_expression_correct_answer_is_win():
    is_valid, is_win, value = evaluate("3+5", 8)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(8)


def test_parens_and_precedence():
    is_valid, is_win, value = evaluate("(3+5)*2", 16)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(16)


def test_exact_fraction_arithmetic_no_float_error():
    # 1/3 * 3 must equal exactly 1 with Fraction, unlike float math.
    is_valid, is_win, value = evaluate("1/3*3", 1)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(1)


def test_fractional_result_not_matching_target():
    is_valid, is_win, value = evaluate("1/3", 1)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(1, 3)


def test_negative_intermediate_result_not_matching_target():
    is_valid, is_win, value = evaluate("3-5", 2)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(-2)


def test_single_number_can_win():
    is_valid, is_win, value = evaluate("5", 5)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(5)


def test_max_depth_parens():
    is_valid, is_win, value = evaluate("(((1+2)*3)-4)+5", 10)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(10)
```
