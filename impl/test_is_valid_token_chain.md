```python
import pytest

from krypto.is_valid_token_chain import is_valid_token_chain


def test_empty_token_chain_is_invalid():
    assert is_valid_token_chain([]) is False


@pytest.mark.parametrize(
    "tokens",
    [
        [0, "+", "+", 1],
        [0, "-", "-", 1],
        [0, "*", "*", 1],
        [0, "/", "/", 1],
        [0, "+", "-", 1],
        [0, "-", "*", 1],
        ["(", "(", 0, "+", "+", 1, ")", ")"],
    ],
)
def test_two_operators_in_a_row_is_invalid(tokens):
    assert is_valid_token_chain(tokens) is False


@pytest.mark.parametrize(
    "tokens",
    [
        [0, 1],
        [0, 1, 2],
        [0, "+", 1, 2],
        ["(", 0, 1, ")"],
    ],
)
def test_two_cards_in_a_row_is_invalid(tokens):
    # Adjacent cards would be joined into one multi-digit number.
    assert is_valid_token_chain(tokens) is False


@pytest.mark.parametrize(
    "tokens",
    [
        ["-", 0, "+", 1],
        ["+", 0],
        ["*", 0],
        ["/", 0],
    ],
)
def test_leading_operator_is_invalid(tokens):
    assert is_valid_token_chain(tokens) is False


@pytest.mark.parametrize(
    "tokens",
    [
        ["(", "-", 0, "+", 1, ")"],
        ["(", "+", 0, ")"],
        [0, "*", "(", "-", 1, ")"],
    ],
)
def test_operator_right_after_open_paren_is_invalid(tokens):
    assert is_valid_token_chain(tokens) is False


@pytest.mark.parametrize(
    "tokens",
    [
        ["(", ")"],
        ["(", "(", ")", ")"],
        [0, "+", "(", ")"],
    ],
)
def test_empty_parentheses_is_invalid(tokens):
    assert is_valid_token_chain(tokens) is False


@pytest.mark.parametrize(
    "tokens",
    [
        [0, "+", 0],
        [0, "+", 1, "*", 0],
        ["(", 0, "+", 1, ")", "*", 0],
    ],
)
def test_repeated_card_index_raises_value_error(tokens):
    # Each card can be used once. The UI prevents a repeat, so one arriving
    # here is a bug in the caller and is deliberately not caught.
    with pytest.raises(ValueError):
        is_valid_token_chain(tokens)


@pytest.mark.parametrize(
    "tokens",
    [
        [-1],
        [0, "+", -1],
    ],
)
def test_negative_card_index_raises_index_error(tokens):
    # hand[-1] would silently return the last card, so a negative index
    # must fail loudly instead.
    with pytest.raises(IndexError):
        is_valid_token_chain(tokens)


@pytest.mark.parametrize(
    "tokens",
    [
        [0, "+", 1],
        [0, "-", 1],
        [0, "*", 1],
        [0, "/", 1],
        [2],
        ["(", 0, "+", 1, ")", "*", 2],
        ["(", 0, "+", 1, ")", "-", 2],
        ["(", "(", "(", 0, "+", 1, ")", "*", 2, ")", "-", 3, ")", "+", 4],
    ],
)
def test_well_formed_chains_are_valid(tokens):
    assert is_valid_token_chain(tokens) is True


@pytest.mark.parametrize(
    "tokens",
    [
        [0, "+"],
        ["(", 0, "+", 1],
        [0, "(", 1, ")"],
    ],
)
def test_other_malformed_chains_are_left_to_eval(tokens):
    # A trailing operator, unbalanced parentheses, and a card next to a
    # parenthesis are not this function's job; evaluate() rejects them.
    assert is_valid_token_chain(tokens) is True
```