import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import pytest
from krypto.append_result import append_result
from krypto.get_history_path import get_history_path

def test_append_result_win():
    # Arrange
    target = 17
    hand: List[int] = [3, 5, 8, 12, 21]
    is_win = True
    cards_used = 4
    time_sec = 42.7

    # Act
    append_result(target, hand, is_win, cards_used, time_sec)

    # Assert
    history_path = get_history_path()
    with open(history_path, 'r') as file:
        lines = file.readlines()
    assert len(lines) == 1
    entry = lines[0].strip()
    expected_entry = f"{datetime.now().isoformat()}  target={target}  hand={','.join(map(str, hand))}  result=WIN  cards_used={cards_used}  time_sec={time_sec}"
    assert entry.startswith(expected_entry.split()[0])  # Check timestamp
    assert entry.endswith(expected_entry.split()[-1])  # Check time_sec

def test_append_result_giveup():
    # Arrange
    target = 9
    hand: List[int] = [1, 2, 7, 15, 19]
    is_win = False
    cards_used = 0
    time_sec = 118.3

    # Act
    append_result(target, hand, is_win, cards_used, time_sec)

    # Assert
    history_path = get_history_path()
    with open(history_path, 'r') as file:
        lines = file.readlines()
    assert len(lines) == 1
    entry = lines[0].strip()
    expected_entry = f"{datetime.now().isoformat()}  target={target}  hand={','.join(map(str, hand))}  result=GIVEUP  cards_used={cards_used}  time_sec={time_sec}"
    assert entry.startswith(expected_entry.split()[0])  # Check timestamp
    assert entry.endswith(expected_entry.split()[-1])  # Check time_sec

def test_append_result_overwrites_existing_file():
    # Arrange
    history_path = get_history_path()
    with open(history_path, 'w') as file:
        file.write("Existing entry\n")

    # Act
    append_result(17, [3, 5, 8, 12, 21], True, 4, 42.7)

    # Assert
    with open(history_path, 'r') as file:
        lines = file.readlines()
    assert len(lines) == 2
    assert lines[0].strip() == "Existing entry"
    assert lines[1].strip().startswith(datetime.now().isoformat())

def test_append_result_handles_file_creation():
    # Arrange
    history_path = get_history_path()
    if history_path.exists():
        history_path.unlink()

    # Act
    append_result(17, [3, 5, 8, 12, 21], True, 4, 42.7)

    # Assert
    assert history_path.exists()
    with open(history_path, 'r') as file:
        lines = file.readlines()
    assert len(lines) == 1
    assert lines[0].strip().startswith(datetime.now().isoformat())

def test_append_result_handles_permission_error():
    # Arrange
    history_path = get_history_path()
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.touch()
    history_path.chmod(0o000)  # Make file read-only

    # Act & Assert
    with pytest.raises(PermissionError):
        append_result(17, [3, 5, 8, 12, 21], True, 4, 42.7)

    # Clean up
    history_path.chmod(0o644)
    history_path.unlink()
