import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import Any
from krypto.load_history import load_history
from krypto.derive_stats import derive_stats
from krypto.derive_best_times import derive_best_times


class StatsWindow:
    """Modal window that displays statistics derived from game history.

    Attributes
    ----------
    parent : tk.Misc
        The parent window (KryptoApp instance).
    window : tk.Toplevel
        The Toplevel window that holds the statistics display.
    """

    def __init__(self, parent: tk.Misc) -> None:
        """Initialize the stats window and load its data.

        Parameters
        ----------
        parent : tk.Misc
            The parent window (KryptoApp instance).

        Raises
        ------
        tk.TclError
            If the Toplevel window cannot be created.
        """
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Stats")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        self.window.transient(parent)
        try:
            self.window.grab_set()
        except tk.TclError:
            # Window is not viewable yet; modality is best-effort.
            pass

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

    def _create_widgets(
        self,
        stats: dict[str, Any],
        best_times: list[dict[str, Any]],
    ) -> None:
        """Create all widgets for the stats window.

        Parameters
        ----------
        stats : dict[str, Any]
            Statistics returned by derive_stats().
        best_times : list[dict[str, Any]]
            Best-time records returned by derive_best_times().
        """
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)
        )

        # Title
        title_label = ttk.Label(main_frame, text="Stats")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Score counts table
        score_counts_frame = ttk.LabelFrame(
            main_frame, text="Final Score", padding="5"
        )
        score_counts_frame.grid(
            row=1, column=0, columnspan=2,
            sticky=(tk.W, tk.E), pady=(0, 10)
        )

        # Header
        header_frame = ttk.Frame(score_counts_frame)
        header_frame.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E)
        )

        score_label = ttk.Label(header_frame, text="Score")
        score_label.grid(row=0, column=0, padx=(0, 100))

        count_label = ttk.Label(header_frame, text="Count")
        count_label.grid(row=0, column=1)

        # Score rows
        score_counts = stats.get('score_counts', [0] * 6)
        for i in range(6):
            score_row = ttk.Frame(score_counts_frame)
            score_row.grid(
                row=i + 1, column=0, sticky=(tk.W, tk.E), pady=2
            )

            score_value = ttk.Label(score_row, text=str(i))
            score_value.grid(row=0, column=0, padx=(0, 100))

            count_value = ttk.Label(
                score_row, text=str(score_counts[i])
            )
            count_value.grid(row=0, column=1)

        # Total games
        total_games_frame = ttk.Frame(main_frame)
        total_games_frame.grid(
            row=2, column=0, columnspan=2,
            sticky=(tk.W, tk.E), pady=(0, 10)
        )

        total_label = ttk.Label(
            total_games_frame, text="Total Games Played"
        )
        total_label.grid(row=0, column=0, padx=(0, 50))

        total_value = ttk.Label(
            total_games_frame, text=str(stats.get('total_games', 0))
        )
        total_value.grid(row=0, column=1)

        # Average score
        avg_score_frame = ttk.Frame(main_frame)
        avg_score_frame.grid(
            row=3, column=0, columnspan=2,
            sticky=(tk.W, tk.E), pady=(0, 10)
        )

        avg_score_label = ttk.Label(
            avg_score_frame, text="Average Final Score"
        )
        avg_score_label.grid(row=0, column=0, padx=(0, 50))

        avg_score = stats.get('average_score')
        avg_score_text = (
            "N/A" if avg_score is None else f"{avg_score:.3f}"
        )
        avg_score_value = ttk.Label(avg_score_frame, text=avg_score_text)
        avg_score_value.grid(row=0, column=1)

        # Average time for 5-card wins
        avg_time_frame = ttk.Frame(main_frame)
        avg_time_frame.grid(
            row=4, column=0, columnspan=2,
            sticky=(tk.W, tk.E), pady=(0, 10)
        )

        avg_time_label = ttk.Label(
            avg_time_frame, text="Average Time (5 card wins only)"
        )
        avg_time_label.grid(row=0, column=0, padx=(0, 50))

        avg_time = stats.get('average_time_5_card')
        avg_time_text = (
            "N/A" if avg_time is None else f"{avg_time:.3f} sec"
        )
        avg_time_value = ttk.Label(avg_time_frame, text=avg_time_text)
        avg_time_value.grid(row=0, column=1)

        # Best times section
        best_times_frame = ttk.LabelFrame(
            main_frame,
            text="Top 10 Best Times (5 card wins only)",
            padding="5",
        )
        best_times_frame.grid(
            row=5, column=0, columnspan=2,
            sticky=(tk.W, tk.E), pady=(0, 10)
        )

        # Best times header
        best_header_frame = ttk.Frame(best_times_frame)
        best_header_frame.grid(
            row=0, column=0, columnspan=4, sticky=(tk.W, tk.E)
        )

        date_label = ttk.Label(
            best_header_frame, text="Date-Time"
        )
        date_label.grid(row=0, column=0, padx=(0, 50))

        target_label = ttk.Label(best_header_frame, text="Target")
        target_label.grid(row=0, column=1, padx=(0, 50))

        hand_label = ttk.Label(best_header_frame, text="Hand")
        hand_label.grid(row=0, column=2, padx=(0, 50))

        time_label = ttk.Label(best_header_frame, text="Time (sec)")
        time_label.grid(row=0, column=3)

        # Best times rows
        for i, record in enumerate(best_times):
            row_frame = ttk.Frame(best_times_frame)
            row_frame.grid(
                row=i + 1, column=0, columnspan=4,
                sticky=(tk.W, tk.E), pady=2
            )

            # Format timestamp
            dt = datetime.fromtimestamp(record.get('timestamp', 0))
            date_str = dt.strftime("%Y-%m-%dT%H:%M:%S")

            row_date = ttk.Label(row_frame, text=date_str)
            row_date.grid(row=0, column=0, padx=(0, 50))

            row_target = ttk.Label(
                row_frame, text=str(record.get('target', 0))
            )
            row_target.grid(row=0, column=1, padx=(0, 50))

            hand_str = ",".join(
                str(card) for card in record.get('hand', [])
            )
            row_hand = ttk.Label(row_frame, text=hand_str)
            row_hand.grid(row=0, column=2, padx=(0, 50))

            time_sec = record.get('time_sec', 0)
            row_time = ttk.Label(row_frame, text=f"{time_sec:.1f}")
            row_time.grid(row=0, column=3)

        # Close button
        close_button = ttk.Button(
            main_frame, text="Close", command=self.window.destroy
        )
        close_button.grid(
            row=6, column=0, columnspan=2, pady=(10, 0)
        )

        # Configure grid weights for proper resizing
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
