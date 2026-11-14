from datetime import datetime                                                                                                 
from pathlib import Path                                                                                                      
                                                                                                                              
import pytest                                                                                                                 
                                                                                                                              
import krypto.load_history as load_history_module                                                                             
from krypto.load_history import load_history                                                                                  
                                                                                                                              
                                                                                                                              
TS_TEXT = "2026-03-15T12:00:00"                                                                                               
TS_UNIX = datetime(2026, 3, 15, 12, 0, 0).timestamp()                                                                         
                                                                                                                              
WIN_LINE = (                                                                                                                  
    f"{TS_TEXT}  target=17  hand=3,5,8,12,21  result=WIN  "                                                                   
    "cards_used=4  time_sec=42.7"                                                                                             
)                                                                                                                             
GIVEUP_LINE = (                                                                                                               
    f"{TS_TEXT}  target=25  hand=1,2,3,4,5  result=GIVEUP  "                                                                  
    "cards_used=0  time_sec=30.5"                                                                                             
)                                                                                                                             
                                                                                                                              
                                                                                                                              
@pytest.fixture                                                                                                               
def history_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:                                                    
    """Point load_history at a temporary history file.                                                                        
                                                                                                                              
    Parameters                                                                                                                
    ----------                                                                                                                
    tmp_path : Path                                                                                                           
        Pytest-provided temporary directory.                                                                                  
    monkeypatch : pytest.MonkeyPatch                                                                                          
        Pytest monkeypatch fixture.                                                                                           
                                                                                                                              
    Returns                                                                                                                   
    -------                                                                                                                   
    Path                                                                                                                      
        Path to the (not yet created) temporary history file.                                                                 
                                                                                                                              
    Raises                                                                                                                    
    ------                                                                                                                    
    None                                                                                                                      
    """                                                                                                                       
    path = tmp_path / "krypto_history.txt"                                                                                    
    monkeypatch.setattr(                                                                                                      
        load_history_module, "get_history_path", lambda: path                                                                 
    )                                                                                                                         
    return path                                                                                                               
                                                                                                                              
                                                                                                                              
def test_nonexistent_file_returns_empty_list(history_file: Path) -> None:                                                     
    """A missing history file yields an empty list.                                                                           
                                                                                                                              
    Parameters                                                                                                                
    ----------                                                                                                                
    history_file : Path                                                                                                       
        Temporary history path that does not exist.                                                                           
                                                                                                                              
    Returns                                                                                                                   
    -------                                                                                                                   
    None                                                                                                                      
                                                                                                                              
    Raises                                                                                                                    
    ------                                                                                                                    
    None                                                                                                                      
    """                                                                                                                       
    assert load_history() == []                                                                                               
                                                                                                                              
                                                                                                                              
def test_empty_file_returns_empty_list(history_file: Path) -> None:                                                           
    """An empty history file yields an empty list.                                                                            
                                                                                                                              
    Parameters                                                                                                                
    ----------                                                                                                                
    history_file : Path                                                                                                       
        Temporary history file with no content.                                                                               
                                                                                                                              
    Returns                                                                                                                   
    -------                                                                                                                   
    None                                                                                                                      
                                                                                                                              
    Raises                                                                                                                    
    ------                                                                                                                    
    None                                                                                                                      
    """                                                                                                                       
    history_file.write_text("")                                                                                               
    assert load_history() == []                                                                                               
                                                                                                                              
                                                                                                                              
def test_parses_win_record(history_file: Path) -> None:                                                                       
    """A WIN line is parsed into the expected dictionary.                                                                     
                                                                                                                              
    Parameters                                                                                                                
    ----------                                                                                                                
    history_file : Path                                                                                                       
        Temporary history file.                                                                                               
                                                                                                                              
    Returns                                                                                                                   
    -------                                                                                                                   
    None                                                                                                                      
                                                                                                                              
    Raises                                                                                                                    
    ------                                                                                                                    
    None                                                                                                                      
    """                                                                                                                       
    history_file.write_text(WIN_LINE + "\n")                                                                                  
    result = load_history()                                                                                                   
                                                                                                                              
    assert len(result) == 1                                                                                                   
    record = result[0]                                                                                                        
    assert record["timestamp"] == TS_UNIX                                                                                     
    assert record["target"] == 17                                                                                             
    assert record["hand"] == [3, 5, 8, 12, 21]                                                                                
    assert record["is_win"] is True                                                                                           
    assert record["cards_used"] == 4                                                                                          
    assert record["time_sec"] == 42.7                                                                                         
                                                                                                                              
                                                                                                                              
def test_giveup_record_is_not_win(history_file: Path) -> None:                                                                
    """A GIVEUP line is parsed with is_win False and score 0.                                                                 
                                                                                                                              
    Parameters                                                                                                                
    ----------                                                                                                                
    history_file : Path                                                                                                       
        Temporary history file.                                                                                               
                                                                                                                              
    Returns                                                                                                                   
    -------                                                                                                                   
    None                                                                                                                      
                                                                                                                              
    Raises                                                                                                                    
    ------                                                                                                                    
    None                                                                                                                      
    """                                                                                                                       
    history_file.write_text(GIVEUP_LINE + "\n")                                                                               
    result = load_history()                                                                                                   
                                                                                                                              
    assert len(result) == 1                                                                                                   
    assert result[0]["is_win"] is False                                                                                       
    assert result[0]["cards_used"] == 0                                                                                       
    assert result[0]["time_sec"] == 30.5                                                                                      
                                                                                                                              
                                                                                                                              
def test_parses_multiple_records_in_order(history_file: Path) -> None:                                                        
    """Multiple lines are returned in file order.                                                                             
                                                                                                                              
    Parameters                                                                                                                
    ----------                                                                                                                
    history_file : Path                                                                                                       
        Temporary history file.                                                                                               
                                                                                                                              
    Returns                                                                                                                   
    -------                                                                                                                   
    None                                                                                                                      
                                                                                                                              
    Raises                                                                                                                    
    ------                                                                                                                    
    None                                                                                                                      
    """                                                                                                                       
    history_file.write_text(WIN_LINE + "\n" + GIVEUP_LINE + "\n")                                                             
    result = load_history()                                                                                                   
                                                                                                                              
    assert len(result) == 2                                                                                                   
    assert result[0]["target"] == 17                                                                                          
    assert result[1]["target"] == 25                                                                                          
                                                                                                                              
                                                                                                                              
def test_skips_blank_lines(history_file: Path) -> None:                                                                       
    """Blank lines between records are ignored.                                                                               
                                                                                                                              
    Parameters                                                                                                                
    ----------                                                                                                                
    history_file : Path                                                                                                       
        Temporary history file.                                                                                               
                                                                                                                              
    Returns                                                                                                                   
    -------                                                                                                                   
    None                                                                                                                      
                                                                                                                              
    Raises                                                                                                                    
    ------                                                                                                                    
    None                                                                                                                      
    """                                                                                                                       
    history_file.write_text(                                                                                                  
        "\n" + WIN_LINE + "\n\n\n" + GIVEUP_LINE + "\n\n"                                                                     
    )                                                                                                                         
    result = load_history()                                                                                                   
                                                                                                                              
    assert len(result) == 2                                                                                                   
                                                                                                                              
                                                                                                                              
@pytest.mark.parametrize(                                                                                                     
    "bad_line",                                                                                                               
    [                                                                                                                         
        "invalid line with no key values",                                                                                    
        f"{TS_TEXT}  target=17  hand=3,5,8,12,21  result=WIN  cards_used=4",                                                  
        f"not-a-timestamp  target=17  hand=3,5  result=WIN  "                                                                 
        "cards_used=1  time_sec=1.0",                                                                                         
        f"{TS_TEXT}  target=abc  hand=3,5  result=WIN  "                                                                      
        "cards_used=1  time_sec=1.0",                                                                                         
        f"{TS_TEXT}  target=17  hand=3,x  result=WIN  "                                                                       
        "cards_used=1  time_sec=1.0",                                                                                         
        f"{TS_TEXT}  target=17  hand=3,5  result=WIN  "                                                                       
        "cards_used=1  time_sec=fast",                                                                                        
    ],                                                                                                                        
)                                                                                                                             
def test_skips_malformed_lines(history_file: Path, bad_line: str) -> None:                                                    
    """Malformed lines are skipped while valid neighbours are kept.                                                           
                                                                                                                              
    Parameters                                                                                                                
    ----------                                                                                                                
    history_file : Path                                                                                                       
        Temporary history file.                                                                                               
    bad_line : str                                                                                                            
        A line that cannot be parsed.                                                                                         
                                                                                                                              
    Returns                                                                                                                   
    -------                                                                                                                   
    None                                                                                                                      
                                                                                                                              
    Raises                                                                                                                    
    ------                                                                                                                    
    None                                                                                                                      
    """                                                                                                                       
    history_file.write_text(                                                                                                  
        WIN_LINE + "\n" + bad_line + "\n" + GIVEUP_LINE + "\n"                                                                
    )                                                                                                                         
    result = load_history()                                                                                                   
                                                                                                                              
    assert len(result) == 2                                                                                                   
    assert result[0]["target"] == 17                                                                                          
    assert result[1]["target"] == 25                                                                                          
                                                                                                                              
                                                                                                                              
def test_unreadable_path_returns_empty_list(                                                                                  
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch                                                                           
) -> None:                                                                                                                    
    """A path that exists but cannot be read as a file yields [].                                                             
                                                                                                                              
    Parameters                                                                                                                
    ----------                                                                                                                
    tmp_path : Path                                                                                                           
        Pytest-provided temporary directory.                                                                                  
    monkeypatch : pytest.MonkeyPatch                                                                                          
        Pytest monkeypatch fixture.                                                                                           
                                                                                                                              
    Returns                                                                                                                   
    -------                                                                                                                   
    None                                                                                                                      
                                                                                                                              
    Raises                                                                                                                    
    ------                                                                                                                    
    None                                                                                                                      
    """                                                                                                                       
    directory = tmp_path / "not_a_file"                                                                                       
    directory.mkdir()                                                                                                         
    monkeypatch.setattr(                                                                                                      
        load_history_module, "get_history_path", lambda: directory                                                            
    )                                                                                                                         
    assert load_history() == []





from datetime import datetime
from pathlib import Path

import pytest

import krypto.load_history as load_history_module
from krypto.load_history import load_history


TS_TEXT = "2026-03-15T12:00:00"
TS_UNIX = datetime(2026, 3, 15, 12, 0, 0).timestamp()

WIN_LINE = (
    f"{TS_TEXT}  target=17  hand=3,5,8,12,21  result=WIN  "
    "cards_used=4  time_sec=42.7"
)
GIVEUP_LINE = (
    f"{TS_TEXT}  target=25  hand=1,2,3,4,5  result=GIVEUP  "
    "cards_used=0  time_sec=30.5"
)


@pytest.fixture
def history_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point load_history at a temporary history file.

    Parameters
    ----------
    tmp_path : Path
        Pytest-provided temporary directory.
    monkeypatch : pytest.MonkeyPatch
        Pytest monkeypatch fixture.

    Returns
    -------
    Path
        Path to the (not yet created) temporary history file.

    Raises
    ------
    None
    """
    path = tmp_path / "krypto_history.txt"
    monkeypatch.setattr(
        load_history_module, "get_history_path", lambda: path
    )
    return path


def test_nonexistent_file_returns_empty_list(history_file: Path) -> None:
    """A missing history file yields an empty list.

    Parameters
    ----------
    history_file : Path
        Temporary history path that does not exist.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    assert load_history() == []


def test_empty_file_returns_empty_list(history_file: Path) -> None:
    """An empty history file yields an empty list.

    Parameters
    ----------
    history_file : Path
        Temporary history file with no content.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    history_file.write_text("")
    assert load_history() == []


def test_parses_win_record(history_file: Path) -> None:
    """A WIN line is parsed into the expected dictionary.

    Parameters
    ----------
    history_file : Path
        Temporary history file.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    history_file.write_text(WIN_LINE + "\n")
    result = load_history()

    assert len(result) == 1
    record = result[0]
    assert record["timestamp"] == TS_UNIX
    assert record["target"] == 17
    assert record["hand"] == [3, 5, 8, 12, 21]
    assert record["is_win"] is True
    assert record["cards_used"] == 4
    assert record["time_sec"] == 42.7


def test_giveup_record_is_not_win(history_file: Path) -> None:
    """A GIVEUP line is parsed with is_win False and score 0.

    Parameters
    ----------
    history_file : Path
        Temporary history file.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    history_file.write_text(GIVEUP_LINE + "\n")
    result = load_history()

    assert len(result) == 1
    assert result[0]["is_win"] is False
    assert result[0]["cards_used"] == 0
    assert result[0]["time_sec"] == 30.5


def test_parses_multiple_records_in_order(history_file: Path) -> None:
    """Multiple lines are returned in file order.

    Parameters
    ----------
    history_file : Path
        Temporary history file.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    history_file.write_text(WIN_LINE + "\n" + GIVEUP_LINE + "\n")
    result = load_history()

    assert len(result) == 2
    assert result[0]["target"] == 17
    assert result[1]["target"] == 25


def test_skips_blank_lines(history_file: Path) -> None:
    """Blank lines between records are ignored.

    Parameters
    ----------
    history_file : Path
        Temporary history file.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    history_file.write_text(
        "\n" + WIN_LINE + "\n\n\n" + GIVEUP_LINE + "\n\n"
    )
    result = load_history()

    assert len(result) == 2


@pytest.mark.parametrize(
    "bad_line",
    [
        "invalid line with no key values",
        f"{TS_TEXT}  target=17  hand=3,5,8,12,21  result=WIN  cards_used=4",
        f"not-a-timestamp  target=17  hand=3,5  result=WIN  "
        "cards_used=1  time_sec=1.0",
        f"{TS_TEXT}  target=abc  hand=3,5  result=WIN  "
        "cards_used=1  time_sec=1.0",
        f"{TS_TEXT}  target=17  hand=3,x  result=WIN  "
        "cards_used=1  time_sec=1.0",
        f"{TS_TEXT}  target=17  hand=3,5  result=WIN  "
        "cards_used=1  time_sec=fast",
    ],
)
def test_skips_malformed_lines(history_file: Path, bad_line: str) -> None:
    """Malformed lines are skipped while valid neighbours are kept.

    Parameters
    ----------
    history_file : Path
        Temporary history file.
    bad_line : str
        A line that cannot be parsed.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    history_file.write_text(
        WIN_LINE + "\n" + bad_line + "\n" + GIVEUP_LINE + "\n"
    )
    result = load_history()

    assert len(result) == 2
    assert result[0]["target"] == 17
    assert result[1]["target"] == 25


def test_unreadable_path_returns_empty_list(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A path that exists but cannot be read as a file yields [].

    Parameters
    ----------
    tmp_path : Path
        Pytest-provided temporary directory.
    monkeypatch : pytest.MonkeyPatch
        Pytest monkeypatch fixture.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    directory = tmp_path / "not_a_file"
    directory.mkdir()
    monkeypatch.setattr(
        load_history_module, "get_history_path", lambda: directory
    )
    assert load_history() == []
