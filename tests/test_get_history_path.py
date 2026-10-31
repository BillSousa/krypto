import pytest
from pathlib import Path
import sys
from src.krypto.get_history_path import get_history_path

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
    
    # Mock __file__ to a path
    __file__ = '/path/to/module.py'
    
    # Expected path when not frozen
    expected_path = Path(__file__).resolve().parent / 'krypto_history.txt'
    
    # Get the history path
    result = get_history_path()
    
    # Assert the result is as expected
    assert result == expected_path
