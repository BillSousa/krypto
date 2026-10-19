## Product Specification
N/A

## Implementation
`evaluate.py` holds a single function, `evaluate(tokens: list[int | str],
hand: list[int], target: int)`, and it is the one place in the codebase
that turns a completed token chain into a correct/wrong/error result
— it owns the entire win-check, not just the arithmetic. It takes the
token chain straight from `KryptoApp`, with no conversion beforehand.
It calls `is_valid_token_chain()` from `is_valid_token_chain.py` first;
if that returns `False`, it returns `(False, False, None)` immediately.
Otherwise it calls `build_expr_string()` from `build_expr_string.py` to
turn the tokens into a string. Every number in that string is rewritten
as `Fraction(<value>)`, so all the arithmetic is exact rational math
instead of floating point: `1/3*3` is exactly 1, a correct answer is
never rejected because of rounding error, and a division by zero raises
a catchable `ZeroDivisionError` instead of producing `inf` or `nan`.
Then it evaluates that string.
```python
import re
from fractions import Fraction

from krypto.build_expr_string import build_expr_string
from krypto.is_valid_token_chain import is_valid_token_chain


def evaluate(
    tokens: list[int | str], hand: list[int], target: int
) -> tuple[bool, bool, Fraction | None]:
    """Evaluate a token chain and check it against the target.

    `tokens` is the token chain exactly as KryptoApp built it from the
    player's clicks: each token is an int (an index into `hand`) or a
    str (one of "+", "-", "*", "/", "(", ")"). evaluate() first checks
    the chain with is_valid_token_chain() and, if that fails, returns
    right away as an invalid expression. Otherwise, it calls
    build_expr_string() to turn the tokens into a plain string (e.g.
    "3+5*2" or "(3+5)*2"), rewrites every number in that string as
    Fraction(<value>), and calls Python's eval() with an empty
    __builtins__ dict. The whole computation therefore happens over
    exact rationals rather than floats, and a genuine divide-by-zero
    raises a catchable ZeroDivisionError instead of producing inf or
    nan. Any exception raised during the rewrite or the eval() call —
    SyntaxError, ZeroDivisionError, TypeError, or anything else — is
    caught and treated as an invalid expression, never allowed to
    propagate to the caller. gui.py is not permitted to contain
    evaluation logic, so it never builds or wraps the string itself.

    Parameters
    ----------
    tokens : list[int | str]
        The clicked tokens, in order, as built by KryptoApp.
    hand : list[int]
        The round's five hand cards, in dealt order. An int token is an
        index into this list.
    target : int
        The round's target number to check the result against.

    Returns
    -------
    tuple[bool, bool, Fraction | None]
        A three-item tuple: ``(is_valid, is_win, value)``.

        - ``is_valid`` is False only when the expression could not be
          computed at all (a token chain rejected by
          is_valid_token_chain(), unbalanced parens, trailing operator,
          division by zero, etc.), in which case ``value`` is None and
          ``is_win`` is always False.
        - Whenever ``is_valid`` is True, ``value`` holds the exact
          Fraction the expression computed — even when it doesn't
          match the target — because the caller needs to show the
          player what their expression actually evaluated to on a
          wrong-answer Submit (SPEC §7.3), not just a bare failure
          message.
        - ``is_win`` is True only when ``is_valid`` is True and
          ``value == Fraction(target)`` exactly. Comparing to target
          lives inside evaluate(), not gui.py, because a win check is
          evaluation logic, not presentation.

    Raises
    ------
    IndexError
        If an int token is positive and outside the range of `hand`. 
        This is a bug in the caller, not a player error, so it is 
        deliberately not caught. Exceptions raised while evaluating the 
        expression (SyntaxError, ZeroDivisionError, TypeError) are caught 
        and reported through the return value.

    Notes
    -----
    evaluate() does not compute cards_used/score. That is derived by
    the caller, by counting the int tokens in the token list.
    """
    if not is_valid_token_chain(tokens):
        return False, False, None

    expr_str = build_expr_string(tokens, hand)
    wrapped = re.sub(r"\d+", lambda m: f"Fraction({m.group()})", expr_str)

    try:
        value = eval(
            wrapped, {"__builtins__": {}}, {"Fraction": Fraction}
        )
    except Exception:
        # Deliberately broad: SyntaxError, ZeroDivisionError,
        # TypeError, and anything else all mean "invalid expression."
        return False, False, None

    is_win = value == Fraction(target)
    return True, is_win, value
```