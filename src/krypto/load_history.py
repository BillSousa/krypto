from datetime import datetime                                                                                                  
from pathlib import Path                                                                                                       
from typing import Any                                                                                                         
                                                                                                                               
from krypto.get_history_path import get_history_path                                                                           
                                                                                                                               
                                                                                                                               
def load_history() -> list[dict[str, Any]]:                                                                                    
    """Load the history file and return one dictionary per round.                                                              
                                                                                                                               
    Each line has the form written by append_result():                                                                         
    ``<ISO timestamp>  target=N  hand=a,b,c,d,e  result=WIN|GIVEUP                                                             
    cards_used=N  time_sec=F``                                                                                                 
                                                                                                                               
    Parameters                                                                                                                 
    ----------                                                                                                                 
    None                                                                                                                       
                                                                                                                               
    Returns                                                                                                                    
    -------                                                                                                                    
    list[dict[str, Any]]                                                                                                       
        One dictionary per valid line, with keys ``timestamp`` (float,                                                         
        Unix time), ``target`` (int), ``hand`` (list[int]), ``is_win``                                                         
        (bool), ``cards_used`` (int), and ``time_sec`` (float). Returns                                                        
        an empty list if the history file does not exist or cannot be                                                          
        read.                                                                                                                  
                                                                                                                               
    Raises                                                                                                                     
    ------                                                                                                                     
    None                                                                                                                       
        Malformed lines are skipped rather than raised.                                                                        
    """                                                                                                                        
    history_path: Path = get_history_path()                                                                                    
    if not history_path.exists():                                                                                              
        return []                                                                                                              
                                                                                                                               
    result: list[dict[str, Any]] = []                                                                                          
    try:                                                                                                                       
        with open(history_path, "r") as file:                                                                                  
            for line in file:                                                                                                  
                line = line.strip()                                                                                            
                if not line:                                                                                                   
                    continue                                                                                                   
                try:                                                                                                           
                    fields = line.split()                                                                                      
                    pairs = dict(item.split("=", 1) for item in fields[1:])                                                    
                    result.append(                                                                                             
                        {                                                                                                      
                            "timestamp": datetime.fromisoformat(                                                               
                                fields[0]                                                                                      
                            ).timestamp(),                                                                                     
                            "target": int(pairs["target"]),                                                                    
                            "hand": [                                                                                          
                                int(card)                                                                                      
                                for card in pairs["hand"].split(",")                                                           
                            ],                                                                                                 
                            "is_win": pairs["result"] == "WIN",                                                                
                            "cards_used": int(pairs["cards_used"]),                                                            
                            "time_sec": float(pairs["time_sec"]),                                                              
                        }                                                                                                      
                    )                                                                                                          
                except (KeyError, ValueError, IndexError):                                                                     
                    continue                                                                                                   
    except OSError:                                                                                                            
        return []                                                                                                              
                                                                                                                               
    return result