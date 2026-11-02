import pytest                                                                                                                                   
                                                                                                                                                
from krypto.derive_best_times import derive_best_times                                                                                          
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
def test_empty_history():                                                                                                                       
                                                                                                                                                
    """Test that derive_best_times returns empty list when history is empty."""                                                                 
                                                                                                                                                
    assert derive_best_times([]) == []                                                                                                          
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
def test_no_5_card_wins():                                                                                                                      
                                                                                                                                                
    """Test that derive_best_times returns empty list when no 5-card wins exist."""                                                             
                                                                                                                                                
    history = [                                                                                                                                 
                                                                                                                                                
        {'is_win': True, 'cards_used': 4, 'time_sec': 10.0},                                                                                    
                                                                                                                                                
        {'is_win': True, 'cards_used': 3, 'time_sec': 15.0},                                                                                    
                                                                                                                                                
        {'is_win': False, 'cards_used': 5, 'time_sec': 20.0},                                                                                   
                                                                                                                                                
    ]                                                                                                                                           
                                                                                                                                                
    assert derive_best_times(history) == []                                                                                                     
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
def test_single_5_card_win():                                                                                                                   
                                                                                                                                                
    """Test that derive_best_times returns single 5-card win."""                                                                                
                                                                                                                                                
    history = [                                                                                                                                 
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 10.0},                                                                                    
                                                                                                                                                
    ]                                                                                                                                           
                                                                                                                                                
    expected = [                                                                                                                                
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 10.0},                                                                                    
                                                                                                                                                
    ]                                                                                                                                           
                                                                                                                                                
    assert derive_best_times(history) == expected                                                                                               
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
def test_multiple_5_card_wins_sorted():                                                                                                         
                                                                                                                                                
    """Test that derive_best_times sorts multiple 5-card wins by time."""                                                                       
                                                                                                                                                
    history = [                                                                                                                                 
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 25.0},                                                                                    
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 10.0},                                                                                    
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 15.0},                                                                                    
                                                                                                                                                
    ]                                                                                                                                           
                                                                                                                                                
    expected = [                                                                                                                                
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 10.0},                                                                                    
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 15.0},                                                                                    
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 25.0},                                                                                    
                                                                                                                                                
    ]                                                                                                                                           
                                                                                                                                                
    assert derive_best_times(history) == expected                                                                                               
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
def test_5_card_wins_with_other_records():                                                                                                      
                                                                                                                                                
    """Test that derive_best_times filters out non-5-card wins and non-wins."""                                                                 
                                                                                                                                                
    history = [                                                                                                                                 
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 10.0},                                                                                    
                                                                                                                                                
        {'is_win': False, 'cards_used': 5, 'time_sec': 15.0},                                                                                   
                                                                                                                                                
        {'is_win': True, 'cards_used': 3, 'time_sec': 20.0},                                                                                    
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 5.0},                                                                                     
                                                                                                                                                
        {'is_win': True, 'cards_used': 4, 'time_sec': 25.0},                                                                                    
                                                                                                                                                
    ]                                                                                                                                           
                                                                                                                                                
    expected = [                                                                                                                                
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 5.0},                                                                                     
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 10.0},                                                                                    
                                                                                                                                                
    ]                                                                                                                                           
                                                                                                                                                
    assert derive_best_times(history) == expected                                                                                               
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
def test_returns_top_10_only():                                                                                                                 
                                                                                                                                                
    """Test that derive_best_times returns only top 10 fastest wins."""                                                                         
                                                                                                                                                
    history = [                                                                                                                                 
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': i * 2.0}                                                                                  
                                                                                                                                                
        for i in range(15)                                                                                                                      
                                                                                                                                                
    ]                                                                                                                                           
                                                                                                                                                
    result = derive_best_times(history)                                                                                                         
                                                                                                                                                
    assert len(result) == 10                                                                                                                    
                                                                                                                                                
    assert result[0]['time_sec'] == 0.0                                                                                                         
                                                                                                                                                
    assert result[-1]['time_sec'] == 18.0                                                                                                       
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                
def test_handles_missing_keys_gracefully():                                                                                                     
                                                                                                                                                
    """Test that derive_best_times handles missing keys gracefully."""                                                                          
                                                                                                                                                
    history = [                                                                                                                                 
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 10.0},                                                                                    
                                                                                                                                                
        {'is_win': True, 'cards_used': 5},  # Missing time_sec                                                                                  
                                                                                                                                                
        {'is_win': True, 'time_sec': 5.0},  # Missing cards_used                                                                                
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 15.0},                                                                                    
                                                                                                                                                
    ]                                                                                                                                           
                                                                                                                                                
    expected = [                                                                                                                                
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 10.0},                                                                                    
                                                                                                                                                
        {'is_win': True, 'cards_used': 5, 'time_sec': 15.0},                                                                                    
                                                                                                                                                
    ]                                                                                                                                           
                                                                                                                                                
    assert derive_best_times(history) == expected





    