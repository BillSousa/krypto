from typing import List, Union

def build_expr_string(tokens: List[Union[int, str]], hand: List[int]) -> str:
    """Build an expression string from tokens and hand.

    Parameters
    ----------
    tokens : List[Union[int, str]]
        The clicked tokens, in order. Each token is an int (an index
        into the hand) or a str (one of "+", "-", "*", "/", "(", ")").
    hand : List[int]
        The round's five hand cards, in dealt order. An int token is an
        index into this list.

    Returns
    -------
    str
        A plain expression string (e.g. "(3+5)*2") built from the tokens
        and hand.

    Raises
    ------
    IndexError
        If an int token is positive and outside the range of `hand`. 
        This is a bug in the caller, not a player error, so it is 
        deliberately not caught.
    """
    expr_str = []
    for token in tokens:
        if isinstance(token, int):
            expr_str.append(str(hand[token]))
        else:
            expr_str.append(token)
    return "".join(expr_str)
