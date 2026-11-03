import pytest                                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
from krypto.get_available_controls import get_available_controls                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
def test_not_started_state():                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    """Test controls when round is not started"""                                                                                                                                  
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    result = get_available_controls("not_started", [])                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    expected = {                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
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
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'start_new_game': True,                                                                                                                                                    
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'stats': True,                                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'how_to_play': True,                                                                                                                                                       
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'exit': True                                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    assert result == expected                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
def test_in_progress_empty_tokens():                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    """Test controls when round is in progress with empty tokens"""                                                                                                                
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    result = get_available_controls("in_progress", [])                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    expected = {                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_0': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_1': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_2': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_3': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_4': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'op': True,                                                                                                                                                                
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'open_paren': True,                                                                                                                                                        
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'close_paren': False,                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'undo': False,                                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'clear': False,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'submit': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'give_up': True,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'start_new_game': False,                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'stats': False,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'how_to_play': False,                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'exit': True                                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    assert result == expected                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
def test_in_progress_with_hand_cards():                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    """Test controls when round is in progress with some hand cards used"""                                                                                                        
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    result = get_available_controls("in_progress", [0, 2])                                                                                                                         
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    expected = {                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_0': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_1': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_2': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_3': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_4': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'op': True,                                                                                                                                                                
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'open_paren': True,                                                                                                                                                        
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'close_paren': False,                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'undo': True,                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'clear': True,                                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'submit': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'give_up': True,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'start_new_game': False,                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'stats': False,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'how_to_play': False,                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'exit': True                                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    assert result == expected                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
def test_in_progress_with_operators():                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    """Test controls when round is in progress with operators"""                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    result = get_available_controls("in_progress", [0, "+", 1])                                                                                                                    
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    expected = {                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_0': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_1': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_2': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_3': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_4': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'op': True,                                                                                                                                                                
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'open_paren': True,                                                                                                                                                        
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'close_paren': False,                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'undo': True,                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'clear': True,                                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'submit': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'give_up': True,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'start_new_game': False,                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'stats': False,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'how_to_play': False,                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'exit': True                                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    assert result == expected                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
def test_in_progress_with_parentheses():                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    """Test controls when round is in progress with parentheses"""                                                                                                                 
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    result = get_available_controls("in_progress", [0, "+", "("])                                                                                                                  
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    expected = {                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_0': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_1': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_2': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_3': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_4': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'op': True,                                                                                                                                                                
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'open_paren': True,                                                                                                                                                        
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'close_paren': True,                                                                                                                                                       
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'undo': True,                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'clear': True,                                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'submit': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'give_up': True,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'start_new_game': False,                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'stats': False,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'how_to_play': False,                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'exit': True                                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    assert result == expected                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
def test_in_progress_with_closed_parentheses():                                                                                                                                    
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    """Test controls when round is in progress with closed parentheses"""                                                                                                          
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    result = get_available_controls("in_progress", [0, "+", "(", 1, ")"])                                                                                                          
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    expected = {                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_0': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_1': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_2': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_3': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_4': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'op': True,                                                                                                                                                                
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'open_paren': True,                                                                                                                                                        
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'close_paren': False,                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'undo': True,                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'clear': True,                                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'submit': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'give_up': True,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'start_new_game': False,                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'stats': False,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'how_to_play': False,                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'exit': True                                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    assert result == expected                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
def test_won_state():                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    """Test controls when round is won"""                                                                                                                                          
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    result = get_available_controls("won", [])                                                                                                                                     
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    expected = {                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
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
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'start_new_game': True,                                                                                                                                                    
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'stats': True,                                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'how_to_play': True,                                                                                                                                                       
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'exit': True                                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    assert result == expected                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
def test_given_up_state():                                                                                                                                                         
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    """Test controls when round is given up"""                                                                                                                                     
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    result = get_available_controls("given_up", [])                                                                                                                                
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    expected = {                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
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
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'start_new_game': True,                                                                                                                                                    
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'stats': True,                                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'how_to_play': True,                                                                                                                                                       
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'exit': True                                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    assert result == expected                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
def test_max_tokens_limit():                                                                                                                                                       
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    """Test controls when round is in progress with maximum tokens (15)"""                                                                                                         
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    # Create a token list with 15 tokens (max allowed)                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    max_tokens = [0, "+", 1, "*", 2, "(", 3, "-", 4, ")", "+", 0, "*", 1, "+"]                                                                                                     
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    result = get_available_controls("in_progress", max_tokens)                                                                                                                     
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    expected = {                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_0': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_1': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_2': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_3': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_4': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'op': False,  # No more operators allowed                                                                                                                                  
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'open_paren': False,  # No more parentheses allowed (max 3)                                                                                                                
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'close_paren': False,  # No more closing parens allowed                                                                                                                    
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'undo': True,                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'clear': True,                                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'submit': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'give_up': True,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'start_new_game': False,                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'stats': False,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'how_to_play': False,                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'exit': True                                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    assert result == expected                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
def test_three_open_parentheses():                                                                                                                                                 
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    """Test controls when round is in progress with three open parentheses"""                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    result = get_available_controls("in_progress", [0, "+", "(", 1, "+", "(", 2, "+", "(", 3])                                                                                     
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    expected = {                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_0': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_1': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_2': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_3': False,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'hand_4': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'op': True,                                                                                                                                                                
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'open_paren': False,  # No more open parentheses allowed (max 3)                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'close_paren': True,                                                                                                                                                       
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'undo': True,                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'clear': True,                                                                                                                                                             
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'submit': True,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'give_up': True,                                                                                                                                                           
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'start_new_game': False,                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'stats': False,                                                                                                                                                            
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'how_to_play': False,                                                                                                                                                      
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
        'exit': True                                                                                                                                                               
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    }                                                                                                                                                                              
                                                                                                                                                                                   
                                                                                                                                                                                   
                                                                                                                                                                                   
    assert result == expected



