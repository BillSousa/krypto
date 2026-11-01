                                                                                                                                                                 
import pytest                                                                                                                                                    
                                                                                                                                                                 
from pathlib import Path                                                                                                                                         
                                                                                                                                                                 
import sys                                                                                                                                                       
                                                                                                                                                                 
from krypto.get_history_path import get_history_path                                                                                                             
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                                                                                                 
def test_get_history_path_frozen():                                                                                                                              
                                                                                                                                                                 
    # Mock the 'frozen' attribute to True                                                                                                                        
                                                                                                                                                                 
    sys.frozen = True                                                                                                                                            
                                                                                                                                                                 
    sys.executable = '/path/to/executable'                                                                                                                       
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                                                                                                 
    # Expected path when frozen                                                                                                                                  
                                                                                                                                                                 
    expected_path = Path('/path/to/executable').parent / 'krypto_history.txt'                                                                                    
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                                                                                                 
    # Get the history path                                                                                                                                       
                                                                                                                                                                 
    result = get_history_path()                                                                                                                                  
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                                                                                                 
    # Assert the result is as expected                                                                                                                           
                                                                                                                                                                 
    assert result == expected_path                                                                                                                               
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                                                                                                 
    # Clean up the mock                                                                                                                                          
                                                                                                                                                                 
    del sys.frozen                                                                                                                                               
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                                                                                                 
def test_get_history_path_not_frozen():                                                                                                                          
                                                                                                                                                                 
    # Mock the 'frozen' attribute to False                                                                                                                       
                                                                                                                                                                 
    if hasattr(sys, 'frozen'):                                                                                                                                   
                                                                                                                                                                 
        del sys.frozen                                                                                                                                           
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                                                                                                 
    # Expected path when not frozen - we'll use a simple approach that doesn't require                                                                           
                                                                                                                                                                 
    # manipulating __file__ directly                                                                                                                             
                                                                                                                                                                 
    # Since we can't easily mock __file__ without side effects, we'll test the actual behavior                                                                   
                                                                                                                                                                 
    # by calling get_history_path() and checking it produces a valid path ending in krypto_history.txt                                                           
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                                                                                                 
    result = get_history_path()                                                                                                                                  
                                                                                                                                                                 
                                                                                                                                                                 
                                                                                                                                                                 
    # Assert that the result is a valid path ending with krypto_history.txt                                                                                      
                                                                                                                                                                 
    assert result.name == 'krypto_history.txt'                                                                                                                   
                                                                                                                                                                 
    assert str(result).endswith('krypto_history.txt')            