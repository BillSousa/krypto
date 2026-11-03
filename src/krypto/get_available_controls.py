from typing import List, Union, Dict                                                                                                                            
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                
def get_available_controls(round_state: str, tokens: List[Union[int, str]]) -> Dict[str, bool]:                                                                 
                                                                                                                                                                
    """                                                                                                                                                         
                                                                                                                                                                
    Determine which controls should be available based on round state and tokens.                                                                               
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                
    Parameters                                                                                                                                                  
                                                                                                                                                                
    ----------                                                                                                                                                  
                                                                                                                                                                
    round_state : str                                                                                                                                           
                                                                                                                                                                
        The current state of the round: "not_started", "in_progress", "won", or "given_up"                                                                      
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                
    tokens : List[Union[int, str]]                                                                                                                              
                                                                                                                                                                
        The ordered list of tokens representing the current expression.                                                                                         
                                                                                                                                                                
        Each token is either an int (hand card index) or a str (operator or parenthesis).                                                                       
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                
    Returns                                                                                                                                                     
                                                                                                                                                                
    -------                                                                                                                                                     
                                                                                                                                                                
    Dict[str, bool]                                                                                                                                             
                                                                                                                                                                
        A dictionary mapping control names to their availability (True = enabled).                                                                              
                                                                                                                                                                
    """                                                                                                                                                                   
                                                                                                                                                                          
                                                                                                                                                                          
                                                                                                                                                                          
    # Initialize all controls as disabled                                                                                                                                 
                                                                                                                                                                          
    controls = {                                                                                                                                                          
                                                                                                                                                                          
        'hand_0': False,                                                                                                                                                  
                                                                                                                                                                          
        'hand_1': False,                                                                                                                                                  
                                                                                                                                                                          
        'hand_2': False,                                                                                                                                                  
                                                                                                                                                                          
        'hand_3': False,                                                                                                                                                  
                                                                                                                                                                          
        'hand_4': False,                                                                                                                                                  
                                                                                                                                                                          
        'op': False,                                                                                                                                                      
                                                                                                                                                                          
        'open_paren': False,                                                                                                                                              
                                                                                                                                                                          
        'close_paren': False,                                                                                                                                             
                                                                                                                                                                          
        'undo': False,                                                                                                                                                    
                                                                                                                                                                          
        'clear': False,                                                                                                                                                   
                                                                                                                                                                          
        'submit': False,                                                                                                                                                  
                                                                                                                                                                          
        'give_up': False,                                                                                                                                                 
                                                                                                                                                                          
        'start_new_game': False,                                                                                                                                          
                                                                                                                                                                          
        'stats': False,                                                                                                                                                   
                                                                                                                                                                          
        'how_to_play': False,                                                                                                                                                      
                                                                                                                                                                                   
        'exit': True  # Exit is always available                                                                                                                                   
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    # If not in progress, only Start New Game, Stats, and How to Play are available                                                                                                
                                                                                                                                                                                   
    if round_state != "in_progress":                                                                                                                                               
                                                                                                                                                                                   
        controls['start_new_game'] = True                                                                                                                                          
                                                                                                                                                                                   
        controls['stats'] = True                                                                                                                                                   
                                                                                                                                                                                   
        controls['how_to_play'] = True                                                                                                                                             
                                                                                                                                                                                   
        return controls                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    # Round is in progress - enable controls based on token state                                                                                                                  
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    # Track used hand cards and parentheses                                                                                                                                        
                                                                                                                                                                                   
    used_hand_indices = set()                                                                                                                                                                                                                                                                            
                                                                                                                                                                                   
    open_parens_count = 0                                                                                                                                                          
                                                                                                                                                                                   
    closed_parens_count = 0                                                                                                                                                        
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    for token in tokens:                                                                                                                                                           
                                                                                                                                                                                   
        if isinstance(token, int):                                                                                                                                                 
                                                                                                                                                                                   
            used_hand_indices.add(token)                                                                                                                                           
                                                                                                                                                                                   
        elif token == '(':                                                                                                                                                         
                                                                                                                                                                                   
            open_parens_count += 1                                                                                                                                                                                                                                                                   
                                                                                                                                                                                   
        elif token == ')':                                                                                                                                                         
                                                                                                                                                                                   
            closed_parens_count += 1                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    # Enable hand card buttons that haven't been used yet                                                                                                                          
                                                                                                                                                                                   
    for i in range(5):                                                                                                                                                             
                                                                                                                                                                                   
        controls[f'hand_{i}'] = i not in used_hand_indices                                                                                                                         
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    # Enable operators if we have less than 15 symbols and there's a previous token                                                                                                
                                                                                                                                                                                   
    if len(tokens) < 15:                                                                                                                                                           
                                                                                                                                                                                   
        controls['op'] = True                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    # Enable open parenthesis if we have less than 15 symbols and less than 3 open parens                                                                                          
                                                                                                                                                                                   
    if len(tokens) < 15 and open_parens_count < 3:                                                                                                                                 
                                                                                                                                                                                   
        controls['open_paren'] = True                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    # Enable close parenthesis if we have less than 15 symbols and there's at least one unclosed paren                                                                             
                                                                                                                                                                                   
    if len(tokens) < 15 and open_parens_count > closed_parens_count:                                                                                                               
                                                                                                                                                                                   
        controls['close_paren'] = True                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    # Enable Undo and Clear if expression is non-empty                                                                                                                             
                                                                                                                                                                                   
    if tokens:                                                                                                                                                                     
                                                                                                                                                                                   
        controls['undo'] = True                                                                                                                                                    
                                                                                                                                                                                   
        controls['clear'] = True                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    # Enable Submit while in progress                                                                                                                                              
                                                                                                                                                                                   
    controls['submit'] = True                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    # Enable Give Up while in progress                                                                                                                                             
                                                                                                                                                                                   
    controls['give_up'] = True                                                                                                                                                     
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    return controls



