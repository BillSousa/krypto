from datetime import datetime                                                                                                  
                                                                                                                               
from pathlib import Path                                                                                                                                                                                                      
from typing import List                                                                                                        
                                                                                                                               
                                                                                                                               
                                                                                                                               
from krypto.get_history_path import get_history_path                                                                           
                                                                                                                               
                                                                                                                               
                                                                                                                               
def append_result(target: int, hand: List[int], is_win: bool, cards_used: int, time_sec: float) -> None:                       
                                                                                                                               
    """                                                                                                                        
    Appends the result of a concluded round to the history file.                                                               
                                                                                                                               
                                                                                                                               
                                                                                                                               
    Parameters:                                                                                                                
                                                                                                                               
    - target (int): The target number for the round.                                                                           
                                                                                                                               
    - hand (List[int]): The list of hand cards dealt.                                                                          
                                                                                                                               
    - is_win (bool): Whether the round was won.                                                                                
                                                                                                                               
    - cards_used (int): The number of cards used in the expression.                                                            
                                                                                                                               
    - time_sec (float): The time taken to complete the round in seconds.                                                       
                                                                                                                               
    """                                                                                                                        
                                                                                                                               
    timestamp = datetime.now().isoformat()                                                                                     
                                                                                                                               
    result = "WIN" if is_win else "GIVEUP"                                                                                     
                                                                                                                               
    hand_str = ",".join(map(str, hand))                                                                                        
                                                                                                                               
    entry = f"{timestamp}  target={target}  hand={hand_str}  result={result}  cards_used={cards_used}  time_sec={time_sec}\n"  
                                                                                                                               
                                                                                                                               
                                                                                                                               
    history_path = get_history_path()                                                                                          
                                                                                                                               
                                                                                                                               
                                                                                                                               
    # Ensure the directory exists                                                                                              
                                                                                                                               
    history_path.parent.mkdir(parents=True, exist_ok=True)                                                                     
                                                                                                                               
                                                                                                                               
                                                                                                                               
    try:                                                                                                                       
                                                                                                                               
        with open(history_path, 'a') as file:                                                                                  
                                                                                                                               
            file.write(entry)                                                                                                  
                                                                                                                               
    except Exception as e:                                                                                                     
                                                                                                                               
        # In production, we might want to log this or handle it differently                                                    
                                                                                                                               
        # For now, we'll re-raise the exception so tests can catch it properly                                                 
                                                                                                                               
        raise e                                                                                                                
                   