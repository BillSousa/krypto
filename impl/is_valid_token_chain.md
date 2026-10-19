## Product Specification
N/A

## Implementation
`is_valid_token_chain.py` holds a single function,
`is_valid_token_chain(tokens: list[int | str]) -> bool`, and it's the
only place token-chain validation rules live — separate from
`evaluate.py` so that new rules discovered later can be added here
without touching `evaluate.py` or `test_evaluate.py`. It checks the
token list itself, before `build_expr_string()` turns it into a string,
because once the tokens are joined into a string the boundaries between
cards are lost. `evaluate()` calls this first and returns
`(False, False, None)` immediately if this returns `False`. 

Currently rejects:
  - an empty list
  - an operator (`+ - * /`) that does not come immediately after a card 
  or a closing parenthesis, meaning an operator at the start or right 
  after an opening parenthesis; Python's `eval()` would otherwise silently 
  accept these as unary plus/minus (e.g. `-3+8`, `(-3+8)`), and a minus 
  created from nothing is not legal Krypto  
  - an operator right after another operator. Python's `eval()` would 
  otherwise silently accept these as unary plus/minus or as the 
  exponent/floor-division operators
  - two cards in a row (two adjacent `int` tokens), which would otherwise 
  be joined into one multi-digit number, e.g. cards 3 and 5 becoming 35
  - empty parentheses (an opening parenthesis immediately followed by a 
  closing one), which `eval()` would otherwise evaluate to an empty tuple 
  instead of a number
  - negative hand indices
  - repeated hand indices

Other malformed placements, such as a trailing operator or a card next 
to a parenthesis, are left to `eval()`, which rejects them. A mis-click 
is not prevented by any live validation (SPEC §5), so this check is what 
catches it.

```python
def is_valid_token_chain(tokens: list[int | str]) -> bool:
    """Check whether a token chain is well-formed enough to evaluate.

    Parameters
    ----------
    tokens : list[int | str]
        The clicked tokens, in order. Each token is an int (an index
        into the hand) or a str (one of "+", "-", "*", "/", "(", ")").

    Returns
    -------
    bool
        False if:
        - tokens is empty
        - an operator token ("+", "-", "*", "/") is not immediately 
        preceded by an int or a ")"
        - two int tokens are adjacent
        - a "(" is immediately followed by a ")" (empty parentheses, 
        which eval() would evaluate to an empty tuple)
        - a leading or post-"(" operator
        - two operators in a row, which would otherwise be silently 
        accepted by Python's eval() as unary plus/minus or as the 
        exponent and floor-division operators
        - adjacent ints
        - negative hand indices
        - repeated hand indices
        True otherwise. This does not guarantee the chain is fully valid 
        (e.g. unbalanced parentheses are not checked here); it only 
        catches cases eval() would not raise on by itself. Any other 
        malformed case is still caught by evaluate()'s own try/except 
        around eval().

    Raises
    ------
    IndexError
        If an int token is negative. This is a bug in the caller, not a 
        player error, so it is deliberately not caught by the try/except 
        in 'evaluate()'.
    """
    if not tokens:
        return False

    operators = ("+", "-", "*", "/")

    hand_idxs = []
    for index, token in enumerate(tokens):

        previous = tokens[index - 1] if index > 0 else None
        
        if token in operators:
            if previous is None:
                return False
            if not isinstance(previous, int) and previous != ")":
                return False

        if isinstance(token, int):
            hand_idxs.append(token)
            if token < 0:
                raise IndexError(f"Negative card index value")
            if isinstance(previous, int):
                return False

        if token == ")" and previous == "(":
            return False

    if len(hand_idxs) != len(set(hand_idxs)):
        raise ValueError(f"Repeated index in token chain")
        
    return True
```