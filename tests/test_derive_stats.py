import pytest                                                                                                                                                         
                                                                                                                                                                      
from unittest.mock import patch                                                                                                                                       
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
from krypto.derive_stats import derive_stats                                                                                                                          
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
def test_empty_history():                                                                                                                                             
                                                                                                                                                                      
    """Test that empty history returns correct default values."""                                                                                                     
                                                                                                                                                                      
    result = derive_stats([])                                                                                                                                         
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
    assert result['score_counts'] == {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}                                                                                             
                                                                                                                                                                      
    assert result['total_games'] == 0                                                                                                                                 
                                                                                                                                                                      
    assert result['average_score'] is None                                                                                                                            
                                                                                                                                                                      
    assert result['average_time_5_card'] is None                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
def test_single_give_up():                                                                                                                                            
                                                                                                                                                                      
    """Test history with a single give-up."""                                                                                                                         
                                                                                                                                                                      
    history = [                                                                                                                                                       
                                                                                                                                                                      
        {                                                                                                                                                             
                                                                                                                                                                      
            'timestamp': 1234567890.0,                                                                                                                                
                                                                                                                                                                      
            'target': 10,                                                                                                                                             
                                                                                                                                                                      
            'hand': [1, 2, 3, 4, 5],                                                                                                                                  
                                                                                                                                                                      
            'is_win': False,                                                                                                                                          
                                                                                                                                                                      
            'cards_used': 0,                                                                                                                                          
                                                                                                                                                                      
            'time_sec': 5.0                                                                                                                                           
                                                                                                                                                                      
        }                                                                                                                                                             
                                                                                                                                                                      
    ]                                                                                                                                                                 
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
    result = derive_stats(history)                                                                                                                                    
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
    assert result['score_counts'] == {0: 1, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}                                                                                             
                                                                                                                                                                      
    assert result['total_games'] == 1                                                                                                                                 
                                                                                                                                                                      
    assert result['average_score'] == 0.0                                                                                                                             
                                                                                                                                                                      
    assert result['average_time_5_card'] is None                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
def test_single_win_5_cards():                                                                                                                                        
                                                                                                                                                                      
    """Test history with a single 5-card win."""                                                                                                                      
                                                                                                                                                                      
    history = [                                                                                                                                                       
                                                                                                                                                                      
        {                                                                                                                                                             
                                                                                                                                                                      
            'timestamp': 1234567890.0,                                                                                                                                
                                                                                                                                                                      
            'target': 10,                                                                                                                                             
                                                                                                                                                                      
            'hand': [1, 2, 3, 4, 5],                                                                                                                                  
                                                                                                                                                                      
            'is_win': True,                                                                                                                                           
                                                                                                                                                                      
            'cards_used': 5,                                                                                                                                          
                                                                                                                                                                      
            'time_sec': 15.0                                                                                                                                          
                                                                                                                                                                      
        }                                                                                                                                                             
                                                                                                                                                                      
    ]                                                                                                                                                                 
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
    result = derive_stats(history)                                                                                                                                    
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
    assert result['score_counts'] == {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 1}                                                                                             
                                                                                                                                                                      
    assert result['total_games'] == 1                                                                                                                                 
                                                                                                                                                                      
    assert result['average_score'] == 5.0                                                                                                                             
                                                                                                                                                                      
    assert result['average_time_5_card'] == 15.0                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
def test_mixed_history():                                                                                                                                             
                                                                                                                                                                      
    """Test history with mixed give-ups and wins."""                                                                                                                  
                                                                                                                                                                      
    history = [                                                                                                                                                       
                                                                                                                                                                      
        {                                                                                                                                                             
                                                                                                                                                                      
            'timestamp': 1234567890.0,                                                                                                                                
                                                                                                                                                                      
            'target': 10,                                                                                                                                             
                                                                                                                                                                      
            'hand': [1, 2, 3, 4, 5],                                                                                                                                  
                                                                                                                                                                      
            'is_win': False,                                                                                                                                          
                                                                                                                                                                      
            'cards_used': 0,                                                                                                                                          
                                                                                                                                                                      
            'time_sec': 5.0                                                                                                                                           
                                                                                                                                                                      
        },                                                                                                                                                            
                                                                                                                                                                      
        {                                                                                                                                                             
                                                                                                                                                                      
            'timestamp': 1234567891.0,                                                                                                                                
                                                                                                                                                                      
            'target': 15,                                                                                                                                             
                                                                                                                                                                      
            'hand': [1, 2, 3, 4, 5],                                                                                                                                  
                                                                                                                                                                      
            'is_win': True,                                                                                                                                           
                                                                                                                                                                      
            'cards_used': 3,                                                                                                                                          
                                                                                                                                                                      
            'time_sec': 10.0                                                                                                                                          
                                                                                                                                                                      
        },                                                                                                                                                            
                                                                                                                                                                      
        {                                                                                                                                                             
                                                                                                                                                                      
            'timestamp': 1234567892.0,                                                                                                                                
                                                                                                                                                                      
            'target': 20,                                                                                                                                             
                                                                                                                                                                      
            'hand': [1, 2, 3, 4, 5],                                                                                                                                  
                                                                                                                                                                      
            'is_win': True,                                                                                                                                           
                                                                                                                                                                      
            'cards_used': 5,                                                                                                                                          
                                                                                                                                                                      
            'time_sec': 20.0                                                                                                                                          
                                                                                                                                                                      
        },                                                                                                                                                            
                                                                                                                                                                      
        {                                                                                                                                                             
                                                                                                                                                                      
            'timestamp': 1234567893.0,                                                                                                                                
                                                                                                                                                                      
            'target': 25,                                                                                                                                             
                                                                                                                                                                      
            'hand': [1, 2, 3, 4, 5],                                                                                                                                  
                                                                                                                                                                      
            'is_win': True,                                                                                                                                           
                                                                                                                                                                      
            'cards_used': 2,                                                                                                                                          
                                                                                                                                                                      
            'time_sec': 8.0                                                                                                                                           
                                                                                                                                                                      
        }                                                                                                                                                             
                                                                                                                                                                      
    ]                                                                                                                                                                 
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
    result = derive_stats(history)                                                                                                                                    
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
    assert result['score_counts'] == {0: 1, 1: 0, 2: 1, 3: 1, 4: 0, 5: 1}                                                                                             
                                                                                                                                                                      
    assert result['total_games'] == 4                                                                                                                                 
                                                                                                                                                                      
    assert result['average_score'] == 2.5  # (0 + 3 + 5 + 2) / 4                                                                                                      
                                                                                                                                                                      
    assert result['average_time_5_card'] == 20.0  # Only the 5-card win                                                                                               
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
def test_no_5_card_wins():                                                                                                                                            
                                                                                                                                                                      
    """Test history with no 5-card wins."""                                                                                                                           
                                                                                                                                                                      
    history = [                                                                                                                                                       
                                                                                                                                                                      
        {                                                                                                                                                             
                                                                                                                                                                      
            'timestamp': 1234567890.0,                                                                                                                                
                                                                                                                                                                      
            'target': 10,                                                                                                                                             
                                                                                                                                                                      
            'hand': [1, 2, 3, 4, 5],                                                                                                                                  
                                                                                                                                                                      
            'is_win': False,                                                                                                                                          
                                                                                                                                                                      
            'cards_used': 0,                                                                                                                                          
                                                                                                                                                                      
            'time_sec': 5.0                                                                                                                                           
                                                                                                                                                                      
        },                                                                                                                                                            
                                                                                                                                                                      
        {                                                                                                                                                             
                                                                                                                                                                      
            'timestamp': 1234567891.0,                                                                                                                                
                                                                                                                                                                      
            'target': 15,                                                                                                                                             
                                                                                                                                                                      
            'hand': [1, 2, 3, 4, 5],                                                                                                                                  
                                                                                                                                                                      
            'is_win': True,                                                                                                                                           
                                                                                                                                                                      
            'cards_used': 3,                                                                                                                                          
                                                                                                                                                                      
            'time_sec': 10.0                                                                                                                                          
                                                                                                                                                                      
        },                                                                                                                                                            
                                                                                                                                                                      
        {                                                                                                                                                             
                                                                                                                                                                      
            'timestamp': 1234567892.0,                                                                                                                                
                                                                                                                                                                      
            'target': 20,                                                                                                                                             
                                                                                                                                                                      
            'hand': [1, 2, 3, 4, 5],                                                                                                                                  
                                                                                                                                                                      
            'is_win': True,                                                                                                                                           
                                                                                                                                                                      
            'cards_used': 2,                                                                                                                                          
                                                                                                                                                                      
            'time_sec': 8.0                                                                                                                                           
                                                                                                                                                                      
        }                                                                                                                                                             
                                                                                                                                                                      
    ]                                                                                                                                                                 
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
    result = derive_stats(history)                                                                                                                                    
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
    assert result['score_counts'] == {0: 1, 1: 0, 2: 1, 3: 1, 4: 0, 5: 0}                                                                                             
                                                                                                                                                                      
    assert result['total_games'] == 3                                                                                                                                 
                                                                                                                                                                      
    assert result['average_score'] == 5/3  # (0 + 3 + 2) / 3                                                                                                          
                                                                                                                                                                      
    assert result['average_time_5_card'] is None                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
def test_all_scores_present():                                                                                                                                        
                                                                                                                                                                      
    """Test that all score counts are present even when zero."""                                                                                                      
                                                                                                                                                                      
    history = [                                                                                                                                                       
                                                                                                                                                                      
        {                                                                                                                                                             
                                                                                                                                                                      
            'timestamp': 1234567890.0,                                                                                                                                
                                                                                                                                                                      
            'target': 10,                                                                                                                                             
                                                                                                                                                                      
            'hand': [1, 2, 3, 4, 5],                                                                                                                                  
                                                                                                                                                                      
            'is_win': True,                                                                                                                                           
                                                                                                                                                                      
            'cards_used': 1,                                                                                                                                          
                                                                                                                                                                      
            'time_sec': 5.0                                                                                                                                           
                                                                                                                                                                      
        },                                                                                                                                                            
                                                                                                                                                                      
        {                                                                                                                                                             
                                                                                                                                                                      
            'timestamp': 1234567891.0,                                                                                                                                
                                                                                                                                                                      
            'target': 15,                                                                                                                                             
                                                                                                                                                                      
            'hand': [1, 2, 3, 4, 5],                                                                                                                                  
                                                                                                                                                                      
            'is_win': True,                                                                                                                                           
                                                                                                                                                                      
            'cards_used': 4,                                                                                                                                          
                                                                                                                                                                      
            'time_sec': 10.0                                                                                                                                          
                                                                                                                                                                      
        }                                                                                                                                                             
                                                                                                                                                                      
    ]                                                                                                                                                                 
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
    result = derive_stats(history)                                                                                                                                    
                                                                                                                                                                      
                                                                                                                                                                      
                                                                                                                                                                      
    assert result['score_counts'] == {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 0}                                                                                             
                                                                                                                                                                      
    assert result['total_games'] == 2                                                                                                                                 
                                                                                                                                                                      
    assert result['average_score'] == 2.5                                                                                                                             
                                                                                                                                                                      
    assert result['average_time_5_card'] is None






