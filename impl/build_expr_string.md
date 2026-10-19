## Product Specification
N/A

## Implementation
`build_expr_string.py` holds a single function,
`build_expr_string(tokens: list[int | str], hand: list[int]) -> str`,
and it's the only place the clicked token list turns into a plain
expression string. It is called by `evaluate()`, not by `KryptoApp`,
and only after `is_valid_token_chain()` has accepted the token list, so
it does no validation of its own. Each token is either an `int` (an
index into `hand`, meaning "this hand card was clicked") or a `str`
(one of `+ - * / ( )`, meaning "this symbol was clicked"). For an `int`
token it looks up `hand[token]` and appends that number's digits; for a
`str` token it appends the symbol as-is. Returns a plain string (e.g.
`"(3+5)*2"`) — digits only, never `Fraction()`-wrapped, since that
wrapping is `evaluate.py`'s job, not this file's. An `int` token that is 
outside the range of `hand` is a bug in the caller, so build_expr_string() 
is deliberately not under a try/except in `evaluate()`. When an `int` 
token is positive and outside the range of `hand`, `IndexError` is raised.
An `int` token that is negative should not get here because of validation 
in `is_valid_token_chain()`.
```python
   <<<function signature>>>
   <<<docstring>>>
   <<<code body>>>
```