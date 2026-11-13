import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import List, Dict
from krypto.load_history import load_history
from krypto.derive_stats import derive_stats
from krypto.derive_best_times import derive_best_times

class StatsWindow:

    """Stats window for displaying game statistics."""

    def __init__(self, parent):

        """Initialize the stats window.

        Args:
            parent: The parent window (KryptoApp instance)
        """

        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Stats")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        # Load and process data
        try:
            history = load_history()
        except Exception:
            history = []

        stats = derive_stats(history)
        best_times = derive_best_times(history)

        # Validate data
        if not isinstance(stats, dict):
            stats = {}
        if not isinstance(best_times, list):
            best_times = []

        # Create the UI
        self._create_widgets(stats, best_times)

    def _create_widgets(self, stats: Dict, best_times: List[Dict]):

        """Create all widgets for the stats window."""

        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="Stats", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Score counts table
        score_counts_frame = ttk.LabelFrame(main_frame, text="Final Score", padding="5")
        score_counts_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Header
        header_frame = ttk.Frame(score_counts_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

        score_label = ttk.Label(header_frame, text="Score", font=("Arial", 10, "bold"))
        score_label.grid(row=0, column=0, padx=(0, 100))

        count_label = ttk.Label(header_frame, text="Count", font=("Arial", 10, "bold"))
        count_label.grid(row=0, column=1)

        # Score rows
        for i in range(6):
            score_row = ttk.Frame(score_counts_frame)
            score_row.grid(row=i+1, column=0, sticky=(tk.W, tk.E), pady=2)

            score_value = ttk.Label(score_row, text=str(i))
            score_value.grid(row=0, column=0, padx=(0, 100))

            count_value = ttk.Label(score_row, text=str(stats.get(i, 0)))
            count_value.grid(row=0, column=1)

        # Total games
        total_games_frame = ttk.Frame(main_frame)
        total_games_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        total_label = ttk.Label(total_games_frame, text="Total Games Played")
        total_label.grid(row=0, column=0, padx=(0, 50))

        total_value = ttk.Label(total_games_frame, text=str(stats.get('total_games', 0)))
        total_value.grid(row=0, column=1)

        # Average score
        avg_score_frame = ttk.Frame(main_frame)
        avg_score_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        avg_score_label = ttk.Label(avg_score_frame, text="Average Final Score")
        avg_score_label.grid(row=0, column=0, padx=(0, 50))

        avg_score_value = ttk.Label(avg_score_frame, text=f"{stats.get('average_score', 'N/A'):.3f}")
        avg_score_value.grid(row=0, column=1)

        # Average time for 5-card wins
        avg_time_frame = ttk.Frame(main_frame)
        avg_time_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        avg_time_label = ttk.Label(avg_time_frame, text="Average Time (5 card wins only)")
        avg_time_label.grid(row=0, column=0, padx=(0, 50))

        avg_time_value = ttk.Label(avg_time_frame, text=f"{stats.get('average_time_5_card', 'N/A'):.3f} sec")
        avg_time_value.grid(row=0, column=1)

        # Best times section
        best_times_frame = ttk.LabelFrame(main_frame, text="Top 10 Best Times (5 card wins only)", padding="5")
        best_times_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Best times header
        best_header_frame = ttk.Frame(best_times_frame)
        best_header_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E))

        date_label = ttk.Label(best_header_frame, text="Date-Time", font=("Arial", 10, "bold"))
        date_label.grid(row=0, column=0, padx=(0, 50))

        target_label = ttk.Label(best_header_frame, text="Target", font=("Arial", 10, "bold"))
        target_label.grid(row=0, column=1, padx=(0, 50))

        hand_label = ttk.Label(best_header_frame, text="Hand", font=("Arial", 10, "bold"))
        hand_label.grid(row=0, column=2, padx=(0, 50))

        time_label = ttk.Label(best_header_frame, text="Time (sec)", font=("Arial", 10, "bold"))
        time_label.grid(row=0, column=3)

        # Best times rows
        for i, record in enumerate(best_times):
            row_frame = ttk.Frame(best_times_frame)
            row_frame.grid(row=i+1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=2)

            # Format timestamp
            dt = datetime.fromtimestamp(record.get('timestamp', 0))
            date_str = dt.strftime("%Y-%m-%dT%H:%M:%S")

            date_label = ttk.Label(row_frame, text=date_str)
            date_label.grid(row=0, column=0, padx=(0, 50))

            target_label = ttk.Label(row_frame, text=str(record.get('target', 0)))
            target_label.grid(row=0, column=1, padx=(0, 50))

            hand_str = ",".join(str(card) for card in record.get('hand', []))
            hand_label = ttk.Label(row_frame, text=hand_str)
            hand_label.grid(row=0, column=2, padx=(0, 50))

            time_label = ttk.Label(row_frame, text=f"{record.get('time_sec', 0):.1f}")
            time_label.grid(row=0, column=3)

        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=self.window.destroy)
        close_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))

        # Configure grid weights for proper resizing
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
