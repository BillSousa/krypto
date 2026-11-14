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
        False if the chain is empty, or if any of the following hold:                                                                                        
                                                                                                                                                             
        - an operator is the first token, or directly follows "("                                                                                            
        - an operator is not preceded by an int or ")"                                                                                                       
        - two operators are adjacent                                                                                                                         
        - two ints are adjacent                                                                                                                              
        - "(" is directly followed by ")" (empty parentheses)                                                                                                
        - a hand index is repeated                                                                                                                           
                                                                                                                                                             
        True otherwise. This does not check every malformed case (for                                                                                        
        example, unbalanced parentheses); evaluate() catches those                                                                                           
        through its own try/except around eval().                                                                                                            
                                                                                                                                                             
    Raises                                                                                                                                                   
    ------                                                                                                                                                   
    IndexError                                                                                                                                               
        If an int token is negative. This is a bug in the caller, not a                                                                                      
        player error, so it is deliberately not caught in evaluate().                                                                                        
    ValueError                                                                                                                                               
        If a hand index appears more than once. This is also a caller                                                                                        
        bug, since the UI prevents repeats.                                                                                                                  
    """

                                                                                                                                                      
    if not tokens:                                                                                                                                           
        return False                                                                                                                                         
                                                                                                                                                             
    operators = ("+", "-", "*", "/")                                                                                                                         
    hand_idxs: list[int] = []                                                                                                                                
                                                                                                                                                             
    for index, token in enumerate(tokens):                                                                                                                   
        previous: int | str | None = tokens[index - 1] if index > 0 else None                                                                                
                                                                                                                                                             
        if token in operators:                                                                                                                               
            if previous is None:                                                                                                                             
                return False                                                                                                                                 
            if not isinstance(previous, int) and previous != ")":                                                                                            
                return False                                                                                                                                 
                                                                                                                                                             
        if isinstance(token, int):                                                                                                                           
            hand_idxs.append(token)                                                                                                                          
            if token < 0:                                                                                                                                    
                raise IndexError("Negative card index value")                                                                                                
            if isinstance(previous, int):                                                                                                                    
                return False                                                                                                                                 
                                                                                                                                                             
        if token == ")" and previous == "(":                                                                                                                 
            return False                                                                                                                                     
                                                                                                                                                             
    if len(hand_idxs) != len(set(hand_idxs)):                                                                                                                
        raise ValueError("Repeated index in token chain")                                                                                                    
                                                                                                                                                             
    return True




