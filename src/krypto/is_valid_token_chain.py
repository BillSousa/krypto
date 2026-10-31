from typing import List, Union

def is_valid_token_chain(tokens: List[Union[int, str]]) -> bool:
    """Check whether a token chain is well-formed enough to evaluate.

    Parameters
    ----------
    tokens : List[Union[int, str]]
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
