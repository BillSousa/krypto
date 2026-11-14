"""Integration test: load_history() feeds derive_stats() and derive_best_times()."""                                                                         
                                                                                                                                                             
from pathlib import Path                                                                                                                                     
                                                                                                                                                             
import pytest                                                                                                                                                
                                                                                                                                                             
from krypto.append_result import append_result                                                                                                               
from krypto.derive_best_times import derive_best_times                                                                                                       
from krypto.derive_stats import derive_stats                                                                                                                 
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
                                                                                                                                                             
                                                                                                                                                             
def _write_sample_history() -> None:                                                                                                                         
    """Write a mixed set of realistic rounds to the history file."""                                                                                         
    append_result(target=24, hand=[1, 2, 3, 4, 5],                                                                                                           
                  is_win=True, cards_used=5, time_sec=20.0)                                                                                                  
    append_result(target=10, hand=[2, 3, 4, 5, 6],                                                                                                           
                  is_win=True, cards_used=5, time_sec=15.0)                                                                                                  
    append_result(target=12, hand=[1, 1, 2, 3, 4],                                                                                                           
                  is_win=True, cards_used=4, time_sec=9.0)                                                                                                   
    append_result(target=7, hand=[5, 6, 7, 8, 9],                                                                                                            
                  is_win=False, cards_used=0, time_sec=40.0)                                                                                                 
                                                                                                                                                             
                                                                                                                                                             
def test_derive_stats_from_loaded_history(history_path: Path) -> None:                                                                                       
    """Stats derived from a loaded file match the written rounds.                                                                                            
                                                                                                                                                             
    Parameters                                                                                                                                               
    ----------                                                                                                                                               
    history_path : Path                                                                                                                                      
        The temporary history file path.                                                                                                                     
    """                                                                                                                                                      
    _write_sample_history()                                                                                                                                  
    stats = derive_stats(load_history())                                                                                                                     
    assert stats["total_games"] == 4                                                                                                                         
    assert stats["score_counts"][5] == 2                                                                                                                     
    assert stats["score_counts"][0] == 1                                                                                                                     
    assert stats["average_score"] == pytest.approx((5 + 5 + 4 + 0) / 4)                                                                                      
    assert stats["average_time_5_card"] == pytest.approx((20.0 + 15.0) / 2)                                                                                  
                                                                                                                                                             
                                                                                                                                                             
def test_derive_best_times_from_loaded_history(                                                                                                              
    history_path: Path,                                                                                                                                      
) -> None:                                                                                                                                                   
    """Only 5-card wins appear, sorted fastest first.                                                                                                        
                                                                                                                                                             
    Parameters                                                                                                                                               
    ----------                                                                                                                                               
    history_path : Path                                                                                                                                      
        The temporary history file path.                                                                                                                     
    """                                                                                                                                                      
    _write_sample_history()                                                                                                                                  
    best = derive_best_times(load_history())                                                                                                                 
    assert [row["time_sec"] for row in best] == [15.0, 20.0]                                                                                                 
                                                                                                                                                             
                                                                                                                                                             
def test_derive_best_times_caps_at_ten(history_path: Path) -> None:                                                                                          
    """Only the 10 fastest 5-card wins are returned.                                                                                                         
                                                                                                                                                             
    Parameters                                                                                                                                               
    ----------                                                                                                                                               
    history_path : Path                                                                                                                                      
        The temporary history file path.                                                                                                                     
    """                                                                                                                                                      
    for i in range(12):                                                                                                                                      
        append_result(target=24, hand=[1, 2, 3, 4, 5],                                                                                                       
                      is_win=True, cards_used=5,                                                                                                             
                      time_sec=float(i + 1))                                                                                                                 
    best = derive_best_times(load_history())                                                                                                                 
    times = [row["time_sec"] for row in best]                                                                                                                
    assert len(times) == 10                                                                                                                                  
    assert times == sorted(times)                                                                                                                            
    assert times[0] == 1.0                                                                                                                                   
    assert times[-1] == 10.0




