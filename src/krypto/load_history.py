                                                                                                                                 
from pathlib import Path                                                                                                         
                                                                                                                                 
import sys                                                                                                                       
                                                                                                                                 
from typing import List, Dict                                                                                                    
                                                                                                                                 
                                                                                                    
from krypto.get_history_path import get_history_path                                                                             
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
def load_history() -> List[Dict]:                                                                                                
                                                                                                                                 
    """                                                                                                                          
                                                                                                                                 
    Loads the history file and returns a list of dictionaries, one per recorded round.                                           
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    Each dictionary contains:                                                                                                    
                                                                                                                                 
    - timestamp (float): Unix timestamp of when the round was concluded                                                          
                                                                                                                                 
    - target (int): The target number for that round                                                                             
                                                                                                                                 
    - hand (list[int]): The 5 hand cards dealt for that round                                                                    
                                                                                                                                 
    - is_win (bool): True if the round was won, False if given up                                                                
                                                                                                                                 
    - cards_used (int): Number of cards used in the solution (1-5) or 0 if given up                                              
                                                                                                                                 
    - time_sec (float): Time taken to complete the round in seconds                                                              
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    Returns:                                                                                                                     
                                                                                                                                 
        List[Dict]: List of dictionaries representing each recorded round.                                                       
                                                                                                                                 
                    Returns an empty list if the history file doesn't exist.                                                     
                                                                                                                                 
    """                                                                                                                          
                                                                                                                                 
    history_path = get_history_path()                                                                                            
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    # If the history file doesn't exist, return an empty list                                                                    
                                                                                                                                 
    if not history_path.exists():                                                                                                
                                                                                                                                 
        return []                                                                                                                
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    result = []                                                                                                                  
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    try:                                                                                                                         
                                                                                                                                 
        with open(history_path, 'r') as f:                                                                                       
                                                                                                                                 
            for line in f:                                                                                                       
                                                                                                                                 
                line = line.strip()                                                                                              
                                                                                                                                 
                if not line:  # Skip empty lines                                                                                 
                                                                                                                                 
                    continue                                                                                                     
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                try:                                                                                                             
                                                                                                                                 
                    # Parse each line according to the format:                                                                   
                                                                                                                                 
                    # timestamp,target,hand,is_win,cards_used,time_sec                                                           
                                                                                                                                 
                    parts = line.split(',')                                                                                      
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                    # Convert timestamp to float                                                                                 
                                                                                                                                 
                    timestamp = float(parts[0])                                                                                  
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                    # Convert target to int                                                                                      
                                                                                                                                 
                    target = int(parts[1])                                                                                       
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                    # Convert hand from comma-separated string to list of ints                                                   
                                                                                                                                 
                    hand = [int(x) for x in parts[2].split('|')]                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                    # Convert is_win from 'WIN'/'GIVEUP' to bool                                                                 
                                                                                                                                 
                    is_win = parts[3] == 'WIN'                                                                                   
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                    # Convert cards_used to int                                                                                  
                                                                                                                                 
                    cards_used = int(parts[4])                                                                                   
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                    # Convert time_sec to float                                                                                  
                                                                                                                                 
                    time_sec = float(parts[5])                                                                                   
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                    result.append({                                                                                              
                                                                                                                                 
                        'timestamp': timestamp,                                                                                  
                                                                                                                                 
                        'target': target,                                                                                        
                                                                                                                                 
                        'hand': hand,                                                                                            
                                                                                                                                 
                        'is_win': is_win,                                                                                        
                                                                                                                                 
                        'cards_used': cards_used,                                                                                
                                                                                                                                 
                        'time_sec': time_sec                                                                                     
                                                                                                                                 
                    })                                                                                                           
                                                                                                                                 
                except (ValueError, IndexError):                                                                                 
                                                                                                                                 
                    # Skip malformed lines rather than crashing                                                                  
                                                                                                                                 
                    continue                                                                                                     
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    except OSError:                                                                                                              
                                                                                                                                 
        # If we can't read the file for any reason, return empty list                                                            
                                                                                                                                 
        return []                                                                                                                
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    return result                                                                                                                





