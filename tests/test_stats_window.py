import tkinter as tk
from tkinter import ttk
from unittest.mock import patch

import pytest

# Import the class we're testing
from krypto.stats_window import StatsWindow


# ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * 
# FIXTURES ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * 

@pytest.fixture
def mock_history_data():
    """Mock history data for testing."""
    return [
        {
            'target': 20,
            'hand': [3, 5, 7, 2, 8],
            'is_win': True,
            'cards_used': 5,
            'time_sec': 45.5
        },
        {
            'target': 15,
            'hand': [1, 2, 3, 4, 5],
            'is_win': True,
            'cards_used': 4,
            'time_sec': 30.2
        },
        {
            'target': 10,
            'hand': [2, 3, 4, 5, 6],
            'is_win': False,
            'cards_used': 0,
            'time_sec': 25.0
        }
    ]


@pytest.fixture
def mock_derive_stats_data():
    """Mock derive_stats function data."""
    return {
        'score_counts': [1, 0, 0, 0, 1, 1],
        'total_games': 3,
        'average_score': 2.0,
        'average_time_5_card': 45.5
    }


@pytest.fixture
def mock_derive_best_times_data():
    """Mock derive_best_times function data."""
    return [
        {
            'timestamp': 1678886400,
            'target': 20,
            'hand': [3, 5, 7, 2, 8],
            'time_sec': 45.5
        }
    ]


@pytest.fixture
def mock_parent_window():
    """Real, hidden Tk root used as the parent window."""
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("No display available for Tkinter tests")
    root.withdraw()
    yield root
    root.destroy()


def _collect_label_texts(widget):
    """Return the text of every ttk.Label under widget, in widget order.

    Parameters
    ----------
    widget : tk.Misc
        The widget whose descendants are searched.

    Returns
    -------
    list[str]
        Label texts in creation order.
    """
    texts = []
    for child in widget.winfo_children():
        if isinstance(child, ttk.Label):
            texts.append(str(child.cget("text")))
        texts.extend(_collect_label_texts(child))
    return texts

# END FIXTURES ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * 
# ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * **



@patch('krypto.stats_window.load_history')
@patch('krypto.stats_window.derive_stats')
@patch('krypto.stats_window.derive_best_times')
def test_stats_window_initialization(
    mock_derive_best_times,
    mock_derive_stats,
    mock_load_history,
    mock_parent_window,
    mock_history_data,
    mock_derive_stats_data,
    mock_derive_best_times_data
):
    """Test that StatsWindow initializes correctly."""
    # Setup mocks
    mock_load_history.return_value = mock_history_data
    mock_derive_stats.return_value = mock_derive_stats_data
    mock_derive_best_times.return_value = mock_derive_best_times_data

    # Map the parent so the transient child window is also mapped
    mock_parent_window.deiconify()
    mock_parent_window.update()

    # Create StatsWindow instance
    stats_window = StatsWindow(mock_parent_window)

    # Verify that the window was created
    assert stats_window.window is not None
    assert stats_window.window.title() == "Stats"
    stats_window.window.deiconify()
    stats_window.window.update()
    assert stats_window.window.geometry().split("+")[0] == "600x700"

    # Verify that the mocks were called
    mock_load_history.assert_called_once()
    mock_derive_stats.assert_called_once_with(mock_history_data)
    mock_derive_best_times.assert_called_once_with(mock_history_data)


@patch('krypto.stats_window.load_history')
@patch('krypto.stats_window.derive_stats')
@patch('krypto.stats_window.derive_best_times')
def test_stats_window_display(
    mock_derive_best_times,
    mock_derive_stats,
    mock_load_history,
    mock_parent_window,
    mock_history_data,
    mock_derive_stats_data,
    mock_derive_best_times_data
):
    """Test that StatsWindow displays data correctly."""
    # Setup mocks
    mock_load_history.return_value = mock_history_data
    mock_derive_stats.return_value = mock_derive_stats_data
    mock_derive_best_times.return_value = mock_derive_best_times_data

    # Create StatsWindow instance
    stats_window = StatsWindow(mock_parent_window)

    # Verify that the window was created and is modal
    assert str(stats_window.window.transient()) == str(mock_parent_window)


@patch('krypto.stats_window.load_history')
@patch('krypto.stats_window.derive_stats')
@patch('krypto.stats_window.derive_best_times')
def test_stats_window_empty_history(
    mock_derive_best_times,
    mock_derive_stats,
    mock_load_history,
    mock_parent_window
):
    """Test that StatsWindow handles empty history correctly."""
    # Setup mocks for empty history
    mock_load_history.return_value = []
    mock_derive_stats.return_value = {
        'score_counts': [0, 0, 0, 0, 0, 0],
        'total_games': 0,
        'average_score': None,
        'average_time_5_card': None
    }
    mock_derive_best_times.return_value = []

    # Create StatsWindow instance
    stats_window = StatsWindow(mock_parent_window)

    # Verify that the window was created
    assert stats_window.window is not None


@patch('krypto.stats_window.load_history')
@patch('krypto.stats_window.derive_stats')
@patch('krypto.stats_window.derive_best_times')
def test_stats_window_shows_na_for_none_averages(
    mock_derive_best_times,
    mock_derive_stats,
    mock_load_history,
    mock_parent_window,
):
    """Test that None averages are displayed as N/A."""
    mock_load_history.return_value = []
    mock_derive_stats.return_value = {
        'score_counts': [0, 0, 0, 0, 0, 0],
        'total_games': 0,
        'average_score': None,
        'average_time_5_card': None
    }
    mock_derive_best_times.return_value = []

    stats_window = StatsWindow(mock_parent_window)

    texts = _collect_label_texts(stats_window.window)
    assert texts.count("N/A") == 2


@patch('krypto.stats_window.load_history')
@patch('krypto.stats_window.derive_stats')
@patch('krypto.stats_window.derive_best_times')
def test_stats_window_shows_score_counts(
    mock_derive_best_times,
    mock_derive_stats,
    mock_load_history,
    mock_parent_window,
):
    """Test that each score row shows its own count."""
    mock_load_history.return_value = []
    mock_derive_stats.return_value = {
        'score_counts': [7, 6, 5, 4, 3, 2],
        'total_games': 27,
        'average_score': None,
        'average_time_5_card': None
    }
    mock_derive_best_times.return_value = []

    stats_window = StatsWindow(mock_parent_window)

    texts = _collect_label_texts(stats_window.window)
    expected = [
        "0", "7", "1", "6", "2", "5",
        "3", "4", "4", "3", "5", "2",
    ]
    assert any(
        texts[i:i + len(expected)] == expected
        for i in range(len(texts))
    )


@patch('krypto.stats_window.load_history')
@patch('krypto.stats_window.derive_stats')
@patch('krypto.stats_window.derive_best_times')
def test_stats_window_with_none_values(
    mock_derive_best_times,
    mock_derive_stats,
    mock_load_history,
    mock_parent_window,
    mock_history_data
):
    """Test that StatsWindow handles None values correctly."""
    # Setup mocks with None values
    mock_load_history.return_value = mock_history_data
    mock_derive_stats.return_value = {
        'score_counts': [0, 0, 0, 0, 0, 0],
        'total_games': 0,
        'average_score': None,
        'average_time_5_card': None
    }
    mock_derive_best_times.return_value = []

    # Create StatsWindow instance
    stats_window = StatsWindow(mock_parent_window)

    # Verify that the window was created
    assert stats_window.window is not None
