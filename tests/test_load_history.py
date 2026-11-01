import os                                                                                                                        
                                                                                                                                 
import tempfile                                                                                                                  
                                                                                                                                 
from pathlib import Path                                                                                                         
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
from krypto.load_history import load_history                                                                                     
                                                                                                                                 
from krypto.get_history_path import get_history_path                                                                             
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
def test_load_history_nonexistent_file():                                                                                        
                                                                                                                                 
    """Test that load_history returns empty list when history file doesn't exist."""                                             
                                                                                                                                 
    # Mock the get_history_path to return a non-existent path                                                                    
                                                                                                                                 
    original_get_history_path = get_history_path                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    def mock_get_history_path():                                                                                                 
                                                                                                                                 
        return Path("/non/existent/path/history.txt")                                                                            
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    # Temporarily replace the function                                                                                           
                                                                                                                                 
    import krypto.load_history as load_history_module                                                                            
                                                                                                                                 
    load_history_module.get_history_path = mock_get_history_path                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    try:                                                                                                                         
                                                                                                                                 
        result = load_history()                                                                                                  
                                                                                                                                 
        assert result == []                                                                                                      
                                                                                                                                 
    finally:                                                                                                                     
                                                                                                                                 
        # Restore original function                                                                                              
                                                                                                                                 
        load_history_module.get_history_path = original_get_history_path                                                         
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
def test_load_history_empty_file():                                                                                              
                                                                                                                                 
    """Test that load_history returns empty list when history file exists but is empty."""                                       
                                                                                                                                 
    # Create a temporary file                                                                                                    
                                                                                                                                 
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:                                                
                                                                                                                                 
        temp_path = f.name                                                                                                       
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    try:                                                                                                                         
                                                                                                                                 
        # Mock get_history_path to return our temp file                                                                          
                                                                                                                                 
        original_get_history_path = get_history_path                                                                             
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        def mock_get_history_path():                                                                                             
                                                                                                                                 
            return Path(temp_path)                                                                                               
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        import krypto.load_history as load_history_module                                                                        
                                                                                                                                 
        load_history_module.get_history_path = mock_get_history_path                                                             
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        try:                                                                                                                     
                                                                                                                                 
            result = load_history()                                                                                              
                                                                                                                                 
            assert result == []                                                                                                  
                                                                                                                                 
        finally:                                                                                                                 
                                                                                                                                 
            # Restore original function                                                                                          
                                                                                                                                 
            load_history_module.get_history_path = original_get_history_path                                                     
                                                                                                                                 
    finally:                                                                                                                     
                                                                                                                                 
        # Clean up temp file                                                                                                     
                                                                                                                                 
        os.unlink(temp_path)                                                                                                     
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
def test_load_history_valid_entries():                                                                                           
                                                                                                                                 
    """Test that load_history correctly parses valid entries."""                                                                 
                                                                                                                                 
    # Create a temporary file with valid entries                                                                                 
                                                                                                                                 
    valid_content = """1678886400.0,17,3|5|8|12|21,WIN,4,42.7                                                                    
                                                                                                                                 
1678886500.0,25,1|2|3|4|5,GIVEUP,0,30.5                                                                                          
                                                                                                                                 
"""                                                                                                                              
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:                                                
                                                                                                                                 
        f.write(valid_content)                                                                                                   
                                                                                                                                 
        temp_path = f.name                                                                                                       
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    try:                                                                                                                         
                                                                                                                                 
        # Mock get_history_path to return our temp file                                                                          
                                                                                                                                 
        original_get_history_path = get_history_path                                                                             
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        def mock_get_history_path():                                                                                             
                                                                                                                                 
            return Path(temp_path)                                                                                               
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        import krypto.load_history as load_history_module                                                                        
                                                                                                                                 
        load_history_module.get_history_path = mock_get_history_path                                                             
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        try:                                                                                                                     
                                                                                                                                 
            result = load_history()                                                                                              
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
            # Check that we got 2 entries                                                                                        
                                                                                                                                 
            assert len(result) == 2                                                                                              
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
            # Check first entry                                                                                                  
                                                                                                                                 
            assert result[0]['timestamp'] == 1678886400.0                                                                        
                                                                                                                                 
            assert result[0]['target'] == 17                                                                                     
                                                                                                                                 
            assert result[0]['hand'] == [3, 5, 8, 12, 21]                                                                        
                                                                                                                                 
            assert result[0]['is_win'] is True                                                                                   
                                                                                                                                 
            assert result[0]['cards_used'] == 4                                                                                  
                                                                                                                                 
            assert result[0]['time_sec'] == 42.7                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
            # Check second entry                                                                                                 
                                                                                                                                 
            assert result[1]['timestamp'] == 1678886500.0                                                                        
                                                                                                                                 
            assert result[1]['target'] == 25                                                                                     
                                                                                                                                 
            assert result[1]['hand'] == [1, 2, 3, 4, 5]                                                                          
                                                                                                                                 
            assert result[1]['is_win'] is False                                                                                  
                                                                                                                                 
            assert result[1]['cards_used'] == 0                                                                                  
                                                                                                                                 
            assert result[1]['time_sec'] == 30.5                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        finally:                                                                                                                 
                                                                                                                                 
            # Restore original function                                                                                          
                                                                                                                                 
            load_history_module.get_history_path = original_get_history_path                                                     
                                                                                                                                 
    finally:                                                                                                                     
                                                                                                                                 
        # Clean up temp file                                                                                                     
                                                                                                                                 
        os.unlink(temp_path)                                                                                                     
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
def test_load_history_malformed_lines():                                                                                         
                                                                                                                                 
    """Test that load_history skips malformed lines and continues parsing."""                                                    
                                                                                                                                 
    # Create a temporary file with some valid and some invalid entries                                                           
                                                                                                                                 
    content_with_errors = """1678886400.0,17,3|5|8|12|21,WIN,4,42.7                                                              
                                                                                                                                 
invalid,line,with,too,few,fields                                                                                                 
                                                                                                                                 
1678886500.0,25,1|2|3|4|5,GIVEUP,0,30.5                                                                                          
                                                                                                                                 
malformed,target,hand,is_win,cards_used,time_sec                                                                                 
                                                                                                                                 
1678886600.0,30,6|7|8|9|10,WIN,5,60.0                                                                                            
                                                                                                                                 
"""                                                                                                                              
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:                                                
                                                                                                                                 
        f.write(content_with_errors)                                                                                             
                                                                                                                                 
        temp_path = f.name                                                                                                       
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    try:                                                                                                                         
                                                                                                                                 
        # Mock get_history_path to return our temp file                                                                          
                                                                                                                                 
        original_get_history_path = get_history_path                                                                             
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        def mock_get_history_path():                                                                                             
                                                                                                                                 
            return Path(temp_path)                                                                                               
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        import krypto.load_history as load_history_module                                                                        
                                                                                                                                 
        load_history_module.get_history_path = mock_get_history_path                                                             
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        try:                                                                                                                     
                                                                                                                                 
            result = load_history()                                                                                              
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
            # Should only parse 2 valid entries, skip the malformed ones                                                         
                                                                                                                                 
            assert len(result) == 3                                                                                              
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
            # Check first valid entry                                                                                            
                                                                                                                                 
            assert result[0]['timestamp'] == 1678886400.0                                                                        
                                                                                                                                 
            assert result[0]['target'] == 17                                                                                     
                                                                                                                                 
            assert result[0]['hand'] == [3, 5, 8, 12, 21]                                                                        
                                                                                                                                 
            assert result[0]['is_win'] is True                                                                                   
                                                                                                                                 
            assert result[0]['cards_used'] == 4                                                                                  
                                                                                                                                 
            assert result[0]['time_sec'] == 42.7                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
            # Check second valid entry                                                                                           
                                                                                                                                 
            assert result[1]['timestamp'] == 1678886500.0                                                                        
                                                                                                                                 
            assert result[1]['target'] == 25                                                                                     
                                                                                                                                 
            assert result[1]['hand'] == [1, 2, 3, 4, 5]                                                                          
                                                                                                                                 
            assert result[1]['is_win'] is False                                                                                  
                                                                                                                                 
            assert result[1]['cards_used'] == 0                                                                                  
                                                                                                                                 
            assert result[1]['time_sec'] == 30.5                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
            # Check third valid entry                                                                                            
                                                                                                                                 
            assert result[2]['timestamp'] == 1678886600.0                                                                        
                                                                                                                                 
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                        
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
            assert result[2]['target'] == 30                                                                                     
                                                                                                                                 
            assert result[2]['hand'] == [6, 7, 8, 9, 10]                                                                         
                                                                                                                                 
            assert result[2]['is_win'] is True                                                                                   
                                                                                                                                 
            assert result[2]['cards_used'] == 5                                                                                  
                                                                                                                                 
            assert result[2]['time_sec'] == 60.0                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        finally:                                                                                                                 
                                                                                                                                 
            # Restore original function                                                                                          
                                                                                                                                 
            load_history_module.get_history_path = original_get_history_path                                                     
                                                                                                                                 
    finally:                                                                                                                     
                                                                                                                                 
        # Clean up temp file                                                                                                     
                                                                                                                                 
        os.unlink(temp_path)                                                                                                     
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
def test_load_history_empty_lines():                                                                                             
                                                                                                                                 
    """Test that load_history handles empty lines correctly."""                                                                  
                                                                                                                                 
    # Create a temporary file with empty lines mixed in                                                                          
                                                                                                                                 
    content_with_empty_lines = """                                                                                               
                                                                                                                                 
1678886400.0,17,3|5|8|12|21,WIN,4,42.7                                                                                           
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
1678886500.0,25,1|2|3|4|5,GIVEUP,0,30.5                                                                                          
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
"""                                                                                                                              
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:                                                
                                                                                                                                 
        f.write(content_with_empty_lines)                                                                                        
                                                                                                                                 
        temp_path = f.name                                                                                                       
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
    try:                                                                                                                         
                                                                                                                                 
        # Mock get_history_path to return our temp file                                                                          
                                                                                                                                 
        original_get_history_path = get_history_path                                                                             
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        def mock_get_history_path():                                                                                             
                                                                                                                                 
            return Path(temp_path)                                                                                               
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        import krypto.load_history as load_history_module                                                                        
                                                                                                                                 
        load_history_module.get_history_path = mock_get_history_path                                                             
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        try:                                                                                                                     
                                                                                                                                 
            result = load_history()                                                                                              
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
            # Should parse 2 valid entries, skip empty lines                                                                     
                                                                                                                                 
            assert len(result) == 2                                                                                              
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
            # Check first entry                                                                                                  
                                                                                                                                 
            assert result[0]['timestamp'] == 1678886400.0                                                                        
                                                                                                                                 
            assert result[0]['target'] == 17                                                                                     
                                                                                                                                 
            assert result[0]['hand'] == [3, 5, 8, 12, 21]                                                                        
                                                                                                                                 
            assert result[0]['is_win'] is True                                                                                   
                                                                                                                                 
            assert result[0]['cards_used'] == 4                                                                                  
                                                                                                                                 
            assert result[0]['time_sec'] == 42.7                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
            # Check second entry                                                                                                 
                                                                                                                                 
            assert result[1]['timestamp'] == 1678886500.0                                                                        
                                                                                                                                 
            assert result[1]['target'] == 25                                                                                     
                                                                                                                                 
            assert result[1]['hand'] == [1, 2, 3, 4, 5]                                                                          
                                                                                                                                 
            assert result[1]['is_win'] is False                                                                                  
                                                                                                                                 
            assert result[1]['cards_used'] == 0                                                                                  
                                                                                                                                 
            assert result[1]['time_sec'] == 30.5                                                                                 
                                                                                                                                 
                                                                                                                                 
                                                                                                                                 
        finally:                                                                                                                 
                                                                                                                                 
            # Restore original function                                                                                          
                                                                                                                                 
            load_history_module.get_history_path = original_get_history_path                                                     
                                                                                                                                 
    finally:                                                                                                                     
                                                                                                                                 
        # Clean up temp file                                                                                                     
                                                                                                                                 
        os.unlink(temp_path)                                                                                                     
                                