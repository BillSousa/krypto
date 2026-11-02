from typing import List, Dict                                                                                                                   
                                                                                                                                                
                                                                                                       
                                                                                                                                                
                                                                                                                                                
def derive_best_times(history: List[Dict]) -> List[Dict]:                                                                                       
                                                                                                                                                
    """                                                                                                                                         
                                                                                                                                                
    Derives the top 10 fastest 5-card wins from the game history.                                                                               
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
    Filters the history to only include wins where exactly 5 cards were used,                                                                   
                                                                                                                                                
    sorts them by time in ascending order, and returns the fastest 10.                                                                          
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
    Parameters:                                                                                                                                 
                                                                                                                                                
        history (List[Dict]): List of dictionaries representing game rounds.                                                                    
                                                                                                                                                
                              Each dict should have 'is_win', 'cards_used', and 'time_sec' keys.                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
    Returns:                                                                                                                                    
                                                                                                                                                
        List[Dict]: List of up to 10 dictionaries representing the fastest 5-card wins.                                                         
                                                                                                                                                
                    Each dict contains 'timestamp', 'target', 'hand' (as list[int]), and 'time_sec'.                                            
                                                                                                                                                
                    Returns an empty list if no qualifying wins exist.                                                                          
                                                                                                                                                
    """                                                                                                                                         
                                                                                                                                                
    # Filter for 5-card wins that have all required fields                                                                                      
                                                                                                                                                
    five_card_wins = []                                                                                                                         
                                                                                                                                                
    for record in history:                                                                                                                      
                                                                                                                                                
        # Check if record has all required fields                                                                                               
                                                                                                                                                
        if (record.get('is_win') is True and                                                                                                    
                                                                                                                                                
            record.get('cards_used') == 5 and                                                                                                   
                                                                                                                                                
            'time_sec' in record):                                                                                                              
                                                                                                                                                
            five_card_wins.append(record)                                                                                                       
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
    # Sort by time (ascending)                                                                                                                  
                                                                                                                                                
    five_card_wins.sort(key=lambda x: x['time_sec'])                                                                                            
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
    # Return top 10                                                                                                                             
                                                                                                                                                
    return five_card_wins[:10]   