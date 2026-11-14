"""Integration test: append_result() writes what load_history() reads."""                                                                                    
                                                                                                                                                             
from pathlib import Path                                                                                                                                     
                                                                                                                                                             
import pytest                                                                                                                                                
                                                                                                                                                             
from krypto.append_result import append_result                                                                                                               
from krypto.load_history import load_history                                                                                                                 
                                                                                                                                                             
                                                                                                                                                             
@pytest.fixture                                                                                                                                              
def history_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:                                                                                   
    """Point both modules at a temporary history file.                                                                                                       
                                                                                                                                                             
    Parameters                                                                                                                                               
    ----------                                                                                                                                               
    tmp_path : Path                                                                                                                                          
        Pytest-provided temporary directory.                                                                                                                 
    monkeypatch : pytest.MonkeyPatch                                                                                                                         
        The pytest monkeypatch fixture.                                                                                                                      
                                                                                                                                                             
    Returns                                                                                                                                                  
    -------                                                                                                                                                  
    Path                                                                                                                                                     
        The temporary history file path.                                                                                                                     
    """                                                                                                                                                      
    path = tmp_path / "krypto_history.txt"                                                                                                                   
    monkeypatch.setattr(                                                                                                                                     
        "krypto.append_result.get_history_path", lambda: path                                                                                                
    )                                                                                                                                                        
    monkeypatch.setattr(                                                                                                                                     
        "krypto.load_history.get_history_path", lambda: path                                                                                                 
    )                                                                                                                                                        
    return path                                                                                                                                              
                                                                                                                                                             
                                                                                                                                                             
def test_round_trip_single_win(history_path: Path) -> None:                                                                                                  
    """A recorded win is read back with the same values.                                                                                                     
                                                                                                                                                             
    Parameters                                                                                                                                               
    ----------                                                                                                                                               
    history_path : Path                                                                                                                                      
        The temporary history file path.                                                                                                                     
    """                                                                                                                                                      
    append_result(                                                                                                                                           
        target=24, hand=[3, 4, 5, 6, 7],                                                                                                                     
        is_win=True, cards_used=5, time_sec=12.5,                                                                                                            
    )                                                                                                                                                        
    history = load_history()                                                                                                                                 
    assert len(history) == 1                                                                                                                                 
    record = history[0]                                                                                                                                      
    assert record["is_win"] is True                                                                                                                          
    assert record["cards_used"] == 5                                                                                                                         
    assert record["time_sec"] == pytest.approx(12.5)                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
def test_round_trip_preserves_order_and_giveup(history_path: Path) -> None:                                                                                  
    """Multiple records are read back in write order, including give-ups.                                                                                    
                                                                                                                                                             
    Parameters                                                                                                                                               
    ----------                                                                                                                                               
    history_path : Path                                                                                                                                      
        The temporary history file path.                                                                                                                     
    """                                                                                                                                                      
    append_result(                                                                                                                                           
        target=10, hand=[1, 2, 3, 4, 5],                                                                                                                     
        is_win=True, cards_used=3, time_sec=8.0,                                                                                                             
    )                                                                                                                                                        
    append_result(                                                                                                                                           
        target=99, hand=[6, 7, 8, 9, 10],                                                                                                                    
        is_win=False, cards_used=0, time_sec=30.0,                                                                                                           
    )                                                                                                                                                        
    history = load_history()                                                                                                                                 
    assert len(history) == 2                                                                                                                                 
    assert history[0]["is_win"] is True                                                                                                                      
    assert history[1]["is_win"] is False                                                                                                                     
    assert history[1]["cards_used"] == 0                                                                                                                     
                                                                                                                                                             
                                                                                                                                                             
def test_load_history_missing_file_returns_empty(                                                                                                            
    history_path: Path,                                                                                                                                      
) -> None:                                                                                                                                                   
    """With no history file yet, load_history() returns an empty list.                                                                                       
                                                                                                                                                             
    Parameters                                                                                                                                               
    ----------                                                                                                                                               
    history_path : Path                                                                                                                                      
        The temporary history file path (not yet created).                                                                                                   
    """                                                                                                                                                      
    assert not history_path.exists()                                                                                                                         
    assert load_history() == []




    