from typing import List, Dict, Union, Optional                                                                                                                     
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
from krypto.load_history import load_history                                                                                                                       
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
def derive_stats(history: List[Dict]) -> Dict[str, Union[int, float, Dict]]:                                                                                       
                                                                                                                                                                   
    """                                                                                                                                                            
                                                                                                                                                                   
    Derives statistics from game history for the Stats screen.                                                                                                     
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
    Args:                                                                                                                                                          
                                                                                                                                                                   
        history: List of dictionaries representing game records from load_history()                                                                                
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
    Returns:                                                                                                                                                       
                                                                                                                                                                   
        Dictionary containing:                                                                                                                                     
                                                                                                                                                                   
        - score_counts: dict with keys 0-5 showing count of games for each score                                                                                   
                                                                                                                                                                   
        - total_games: int, total number of records                                                                                                                
                                                                                                                                                                   
        - average_score: float, mean of cards_used across all records (with give-ups as 0)                                                                         
                                                                                                                                                                   
        - average_time_5_card: float, mean time_sec across only 5-card wins, or None if no 5-card wins                                                             
                                                                                                                                                                   
    """                                                                                                                                                            
                                                                                                                                                                   
    # Initialize result structure                                                                                                                                  
                                                                                                                                                                   
    result = {                                                                                                                                                     
                                                                                                                                                                   
        'score_counts': {i: 0 for i in range(6)},  # 0 through 5                                                                                                   
                                                                                                                                                                   
        'total_games': 0,                                                                                                                                          
                                                                                                                                                                   
        'average_score': None,                                                                                                                                     
                                                                                                                                                                   
        'average_time_5_card': None                                                                                                                                
                                                                                                                                                                   
    }                                                                                                                                                              
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
    # Handle empty history case                                                                                                                                    
                                                                                                                                                                   
    if not history:                                                                                                                                                
                                                                                                                                                                   
        return result                                                                                                                                              
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
    # Set total games count                                                                                                                                        
                                                                                                                                                                   
    result['total_games'] = len(history)                                                                                                                           
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
    # Calculate score counts and sum for average score                                                                                                             
                                                                                                                                                                   
    total_score = 0                                                                                                                                                
                                                                                                                                                                   
    five_card_wins = []                                                                                                                                            
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
    for record in history:                                                                                                                                         
                                                                                                                                                                   
        cards_used = record['cards_used']                                                                                                                          
                                                                                                                                                                   
        is_win = record['is_win']                                                                                                                                  
                                                                                                                                                                   
        time_sec = record['time_sec']                                                                                                                              
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
        # Update score count (give-ups are counted as 0)                                                                                                           
                                                                                                                                                                   
        result['score_counts'][cards_used] += 1                                                                                                                    
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
        # Add to total score for average calculation                                                                                                               
                                                                                                                                                                   
        total_score += cards_used                                                                                                                                  
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
        # Collect 5-card wins for average time calculation                                                                                                         
                                                                                                                                                                   
        if is_win and cards_used == 5:                                                                                                                             
                                                                                                                                                                   
            five_card_wins.append(time_sec)                                                                                                                        
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
    # Calculate average score (mean of all cards_used, including give-ups as 0)                                                                                    
                                                                                                                                                                   
    result['average_score'] = total_score / len(history)                                                                                                           
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
    # Calculate average time for 5-card wins if any exist                                                                                                          
                                                                                                                                                                   
    if five_card_wins:                                                                                                                                             
                                                                                                                                                                   
        result['average_time_5_card'] = sum(five_card_wins) / len(five_card_wins)                                                                                  
                                                                                                                                                                   
                                                                                                                                                                   
                                                                                                                                                                   
    return result




