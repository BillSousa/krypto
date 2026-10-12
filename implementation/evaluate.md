`evaluate.py` holds a single function, `evaluate(expr_str: str, target:
int)`, and it is the one place in the codebase that turns a completed
expression into a pass/fail/wrong-answer result — it owns the entire
win-check, not just the arithmetic. It calls `is_valid_expr_str()` from
`is_valid_expr_str.py` first; if that returns `False`, it returns
`(False, False, None)` immediately without calling `eval()`.
```python
import re
from fractions import Fraction

from krypto.is_valid_expr_str import is_valid_expr_str


def evaluate(
    expr_str: str, target: int
) -> tuple[bool, bool, Fraction | None]:
    """Evaluate an expression string and check it against the target.

    `expr_str` is a plain string exactly as the digits, operators, and
    parentheses were clicked (e.g. "3+5*2" or "(3+5)*2") — never
    Fraction()-wrapped by the caller, since that wrapping is
    evaluate()'s own job, not gui.py's (gui.py is not permitted to
    contain evaluation logic). Internally, evaluate() rewrites every
    number in expr_str as Fraction(<value>) before calling Python's
    eval() with an empty __builtins__ dict, so the whole computation
    happens over exact rationals rather than floats, and a genuine
    divide-by-zero raises a catchable ZeroDivisionError instead of
    producing inf or nan. expr_str is checked with is_valid_expr_str()
    first (empty string, adjacent operators) and treated as invalid
    immediately, without attempting to eval() it at all, if that check
    fails. Any exception raised during the rewrite or the eval() call —
    SyntaxError, ZeroDivisionError, TypeError, or anything else — is
    caught and treated as an invalid expression, never allowed to
    propagate to the caller.

    Parameters
    ----------
    expr_str : str
        The clicked expression, exactly as built (e.g. "(3+5)*2").
        Never pre-wrapped in Fraction() by the caller.
    target : int
        The round's target number to check the result against.

    Returns
    -------
    tuple[bool, bool, Fraction | None]
        A three-item tuple: ``(is_valid, is_win, value)``.

        - ``is_valid`` is False only when the expression could not be
          computed at all (empty string, unbalanced parens, trailing
          operator, division by zero, etc.), in which case ``value``
          is None and ``is_win`` is always False.
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
    None
        All exceptions raised while parsing or evaluating expr_str are
        caught internally and reported through the return value, never
        propagated to the caller.

    Notes
    -----
    evaluate() does not compute cards_used/score — it only sees the
    flattened text and has no way to tell which digits came from which
    hand-card button, so that has to be derived elsewhere, from the
    token list, not from this string.
    """
    if not is_valid_expr_str(expr_str):
        return False, False, None

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
