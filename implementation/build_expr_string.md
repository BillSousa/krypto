`build_expr_string.py` holds a single function,
`build_expr_string(tokens: list[int | str], hand: list[int]) -> str`,
and it's the only place the clicked token list turns into a plain
expression string. Each token is either an `int` (an index into
`hand`, meaning "this hand card was clicked") or a `str` (one of
`+ - * / ( )`, meaning "this symbol was clicked"). For an `int` token
it looks up `hand[token]` and appends that number's digits; for a
`str` token it appends the symbol as-is. Returns a plain string (e.g.
`"(3+5)*2"`) — digits only, never `Fraction()`-wrapped, since that
wrapping is `evaluate.py`'s job, not this file's.
```python
   <<<function signature>>>
   <<<docstring>>>
   <<<code body>>>
```
