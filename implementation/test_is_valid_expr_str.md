```python
import pytest

from krypto.is_valid_expr_str import is_valid_expr_str


def test_empty_string_is_invalid():
    assert is_valid_expr_str("") is False


@pytest.mark.parametrize(
    "expr_str",
    [
        "3++5",
        "3--5",
        "3**5",
        "3//5",
        "3+-5",
        "3-*5",
        "((3++5))",
    ],
)
def test_adjacent_operators_are_invalid(expr_str):
    assert is_valid_expr_str(expr_str) is False


@pytest.mark.parametrize(
    "expr_str",
    [
        "3+5",
        "3-5",
        "3*5",
        "3/5",
        "(3+5)*2",
        "(((1+2)*3)-4)+5",
        "12+25",
        "5",
    ],
)
def test_well_formed_expressions_are_valid(expr_str):
    assert is_valid_expr_str(expr_str) is True
```
