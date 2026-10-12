`is_valid_expr_str.py` holds a single function,
`is_valid_expr_str(expr_str: str) -> bool`, and it's the only place
expr_str validation rules live — separate from `evaluate.py` so that
new rules discovered later can be added here without touching
`evaluate.py` or `test_evaluate.py`. `evaluate()` calls it first and
returns `(False, False, None)` immediately, without calling `eval()`
at all, if it returns `False`. Currently rejects: an empty string, and
any two adjacent characters from `+-*/` (e.g. `"3++5"`, `"3--5"`,
`"3**5"`, `"3//5"`) — Python's `eval()` would otherwise silently accept
these as unary plus/minus or as the exponent/floor-division operators,
producing a wrong result instead of failing, since a mis-click or
double-click on an operator button isn't prevented by any live
validation (SPEC §4).
```python
import re


def is_valid_expr_str(expr_str: str) -> bool:
    """Check whether an expression string is well-formed enough to
    attempt evaluation.

    Parameters
    ----------
    expr_str : str
        The clicked expression, exactly as built (e.g. "(3+5)*2").

    Returns
    -------
    bool
        False if expr_str is empty, or contains two or more adjacent
        characters from "+-*/" (e.g. "3++5", "3--5", "3**5", "3//5")
        — sequences Python's eval() would otherwise silently accept as
        unary plus/minus, or as the exponent/floor-division operators,
        instead of rejecting as malformed. True otherwise. This does
        not guarantee expr_str is fully valid Python syntax (e.g.
        unbalanced parentheses are not checked here); it only catches
        cases eval() would not raise on by itself. Any other malformed
        case is still caught by evaluate()'s own try/except around
        eval().

    Raises
    ------
    None
    """
    if not expr_str:
        return False

    if re.search(r"[+\-*/]{2,}", expr_str):
        return False

    return True
```
