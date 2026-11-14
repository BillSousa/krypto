import time
import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox

from krypto.append_result import append_result
from krypto.build_expr_string import build_expr_string
from krypto.deal import deal
from krypto.evaluate import evaluate
from krypto.get_available_controls import get_available_controls
from krypto.stats_window import StatsWindow


class KryptoApp(tk.Tk):
    """Top-level Tkinter window for the Krypto card game.

    Owns the round state, the current target and hand, the ordered
    token list, and every widget. Delegates dealing, evaluation,
    persistence, and control availability to other modules.

    Attributes
    ----------
    TIMER_INTERVAL_MS : int
        Milliseconds between stopwatch display updates.
    OPERATORS : tuple[str, ...]
        The arithmetic operator symbols shown as buttons.
    HOW_TO_PLAY_TEXT : str
        Rules text shown in the How to Play window (SPEC §7.7).
    """

    TIMER_INTERVAL_MS: int = 100
    OPERATORS: tuple[str, ...] = ("+", "-", "*", "/")
    HOW_TO_PLAY_TEXT: str = "\n".join(
        (
            "- Each round deals a target number and five hand cards",
            "  (1 to 25) from a 56-card deck.",
            "- Combine the hand cards with the arithmetic operators",
            "  (+ - * /) and parentheses to make an expression that",
            "  equals the target exactly.",
            "- Each hand card can only be used once. You do not have",
            "  to use all five cards. Your score is the number of",
            "  cards you used, from 1 to 5.",
            "- Negative and fractional values are allowed in the",
            "  middle of a calculation. Only the final result has",
            "  to equal the target.",
            "- Give Up and Exit end the round with a score of 0.",
            "- The timer counts up from the moment you click Start",
            "  New Game, and stops when you solve the round or give",
            "  up.",
        )
    )

    def __init__(self) -> None:
        """Create the main window and start in the "not_started" state.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        super().__init__()
        self.title("Krypto")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._on_exit)

        self._round_state: str = "not_started"
        self._target: int = 0
        self._hand: list[int] = []
        self._tokens: list[int | str] = []
        self._start_time: float = 0.0
        self._timer_job: str | None = None
        self._stats_window: StatsWindow | None = None

        self._buttons: dict[str, tk.Button] = {}
        self._op_buttons: list[tk.Button] = []
        self._target_var = tk.StringVar(self, value="Target: -")
        self._time_var = tk.StringVar(self, value="Time: 00:00.0")
        self._expr_var = tk.StringVar(self, value="")
        self._status_var = tk.StringVar(self, value="")

        self._build_widgets()
        self._refresh_controls()

    def _make_button(
        self, parent: tk.Misc, text: str, command: Callable[[], None]
    ) -> tk.Button:
        """Create a plain, unpacked button.

        Parameters
        ----------
        parent : tk.Misc
            The widget that will contain the button.
        text : str
            The label shown on the button.
        command : Callable[[], None]
            The function called when the button is clicked.

        Returns
        -------
        tk.Button
            The newly created button.

        Raises
        ------
        None
        """
        return tk.Button(parent, text=text, command=command)

    def _build_widgets(self) -> None:
        """Create every widget in the game layout (SPEC §7.1).

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=10, pady=(10, 5))
        tk.Label(top, text="Krypto").pack(side=tk.LEFT)
        self._buttons["how_to_play"] = self._make_button(
            top, "How to Play", self._on_how_to_play
        )
        self._buttons["how_to_play"].pack(side=tk.RIGHT, padx=2)
        self._buttons["stats"] = self._make_button(
            top, "Stats", self._on_stats
        )
        self._buttons["stats"].pack(side=tk.RIGHT, padx=2)

        info = tk.Frame(self)
        info.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(info, textvariable=self._target_var).pack(side=tk.LEFT)
        tk.Label(info, textvariable=self._time_var).pack(side=tk.RIGHT)

        hand_row = tk.Frame(self)
        hand_row.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(hand_row, text="Hand:").pack(side=tk.LEFT)
        for index in range(5):
            button = self._make_button(
                hand_row, "-", lambda i=index: self._on_hand_click(i)
            )
            button.pack(side=tk.LEFT, padx=2)
            self._buttons[f"hand_{index}"] = button

        ops_row = tk.Frame(self)
        ops_row.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(ops_row, text="Ops:").pack(side=tk.LEFT)
        for symbol in self.OPERATORS:
            button = self._make_button(
                ops_row, symbol, lambda s=symbol: self._on_symbol_click(s)
            )
            button.pack(side=tk.LEFT, padx=2)
            self._op_buttons.append(button)
        self._buttons["open_paren"] = self._make_button(
            ops_row, "(", lambda: self._on_symbol_click("(")
        )
        self._buttons["open_paren"].pack(side=tk.LEFT, padx=(10, 2))
        self._buttons["close_paren"] = self._make_button(
            ops_row, ")", lambda: self._on_symbol_click(")")
        )
        self._buttons["close_paren"].pack(side=tk.LEFT, padx=2)

        expr_row = tk.Frame(self)
        expr_row.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(expr_row, text="Expr:").pack(side=tk.LEFT)
        tk.Label(expr_row, textvariable=self._expr_var, width=40,
                 anchor="w").pack(side=tk.LEFT, padx=2)

        action_row = tk.Frame(self)
        action_row.pack(fill=tk.X, padx=10, pady=5)
        self._buttons["clear"] = self._make_button(
            action_row, "Clear", self._on_clear
        )
        self._buttons["undo"] = self._make_button(
            action_row, "Undo", self._on_undo
        )
        self._buttons["submit"] = self._make_button(
            action_row, "Submit", self._on_submit
        )
        self._buttons["give_up"] = self._make_button(
            action_row, "Give Up", self._on_give_up
        )
        for name in ("clear", "undo", "submit", "give_up"):
            self._buttons[name].pack(side=tk.LEFT, padx=6)

        status = tk.Frame(self)
        status.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(status, textvariable=self._status_var).pack(side=tk.LEFT)

        bottom = tk.Frame(self)
        bottom.pack(fill=tk.X, padx=10, pady=(5, 10))
        self._buttons["start_new_game"] = self._make_button(
            bottom, "Start New Game", self._on_start_new_game
        )
        self._buttons["start_new_game"].pack(side=tk.LEFT, padx=6)
        self._buttons["exit"] = self._make_button(
            bottom, "Exit", self._on_exit
        )
        self._buttons["exit"].pack(side=tk.LEFT, padx=6)

    def _refresh_controls(self) -> None:
        """Apply get_available_controls() to every button and the expression.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        controls = get_available_controls(self._round_state, self._tokens)
        for name, button in self._buttons.items():
            enabled = controls[name]
            button.config(state=tk.NORMAL if enabled else tk.DISABLED)
        for button in self._op_buttons:
            button.config(state=tk.NORMAL if controls["op"] else tk.DISABLED)

        if self._tokens:
            self._expr_var.set(build_expr_string(self._tokens, self._hand))
        else:
            self._expr_var.set("")

    def _update_timer_display(self, elapsed: float) -> None:
        """Show an elapsed time as MM:SS.t in the timer label.

        Parameters
        ----------
        elapsed : float
            Elapsed seconds since the round started.

        Returns
        -------
        None

        Raises
        ------
        None
        """
        tenths = int(elapsed * 10)
        minutes, rest = divmod(tenths, 600)
        seconds, tenth = divmod(rest, 10)
        self._time_var.set(f"Time: {minutes:02d}:{seconds:02d}.{tenth}")

    def _tick(self) -> None:
        """Update the stopwatch display and schedule the next update.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self._update_timer_display(time.monotonic() - self._start_time)
        self._timer_job = self.after(self.TIMER_INTERVAL_MS, self._tick)

    def _count_cards_used(self) -> int:
        """Count the hand cards placed in the current expression.

        Parameters
        ----------
        None

        Returns
        -------
        int
            The number of int tokens in the token list.

        Raises
        ------
        None
        """
        return sum(1 for token in self._tokens if isinstance(token, int))

    def _record_result(
        self, is_win: bool, cards_used: int, time_sec: float
    ) -> None:
        """Save a concluded round to history, reporting any save failure.

        Parameters
        ----------
        is_win : bool
            Whether the round was won.
        cards_used : int
            The score to record (0 for a give-up or exit).
        time_sec : float
            The round duration in seconds.

        Returns
        -------
        None

        Raises
        ------
        None
            OSError from append_result() is shown to the player instead.
        """
        try:
            append_result(
                self._target, self._hand, is_win, cards_used, time_sec
            )
        except OSError as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save the round to history:\n{error}",
                parent=self,
            )

    def _finish_round(self, new_state: str, is_win: bool) -> float:
        """Stop the timer, record the round, and freeze the screen.

        Parameters
        ----------
        new_state : str
            The round state after conclusion: "won" or "given_up".
        is_win : bool
            Whether the round was won. A non-win scores 0.

        Returns
        -------
        float
            The round duration in seconds.

        Raises
        ------
        None
        """
        time_sec = time.monotonic() - self._start_time
        if self._timer_job is not None:
            self.after_cancel(self._timer_job)
            self._timer_job = None

        cards_used = self._count_cards_used() if is_win else 0
        self._record_result(is_win, cards_used, time_sec)
        self._update_timer_display(time_sec)
        self._round_state = new_state
        self._refresh_controls()
        return time_sec

    def _on_start_new_game(self) -> None:
        """Deal a fresh round and start the stopwatch.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self._target, self._hand = deal()
        self._tokens = []
        self._round_state = "in_progress"
        self._target_var.set(f"Target: {self._target}")
        for index, card in enumerate(self._hand):
            self._buttons[f"hand_{index}"].config(text=str(card))
        self._status_var.set("")
        self._start_time = time.monotonic()
        self._update_timer_display(0.0)
        self._timer_job = self.after(self.TIMER_INTERVAL_MS, self._tick)
        self._refresh_controls()

    def _on_hand_click(self, index: int) -> None:
        """Append a hand card to the expression.

        Parameters
        ----------
        index : int
            The position of the clicked card in the hand.

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self._tokens.append(index)
        self._refresh_controls()

    def _on_symbol_click(self, symbol: str) -> None:
        """Append an operator or parenthesis to the expression.

        Parameters
        ----------
        symbol : str
            One of "+", "-", "*", "/", "(", or ")".

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self._tokens.append(symbol)
        self._refresh_controls()

    def _on_undo(self) -> None:
        """Remove the most recently placed token.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        if self._tokens:
            self._tokens.pop()
        self._refresh_controls()

    def _on_clear(self) -> None:
        """Remove every token from the expression.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self._tokens = []
        self._refresh_controls()

    def _on_submit(self) -> None:
        """Evaluate the expression and win the round if it matches.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        is_valid, is_win, value = evaluate(
            self._tokens, self._hand, self._target
        )
        if not is_valid:
            self._status_var.set(
                "Invalid expression. Check the operators and parentheses."
            )
            return
        if not is_win:
            self._status_var.set(
                f"Your expression equals {value}, not {self._target}."
            )
            return

        cards_used = self._count_cards_used()
        time_sec = self._finish_round("won", True)
        self._status_var.set(
            f"Solved with {cards_used} cards in {time_sec:.1f}s!"
        )

    def _on_give_up(self) -> None:
        """Confirm and end the round with a score of 0.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        confirmed = messagebox.askyesno(
            "Give Up",
            "Give up this round? It will be recorded with a score of 0.",
            parent=self,
        )
        if not confirmed:
            return
        self._finish_round("given_up", False)
        self._status_var.set(
            "Round given up. Click Start New Game to play again."
        )

    def _on_exit(self) -> None:
        """Close the app, recording a give-up if a round is in progress.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        if self._round_state == "in_progress":
            confirmed = messagebox.askyesno(
                "Exit",
                "Exit now? The round will be recorded with a score of 0.",
                parent=self,
            )
            if not confirmed:
                return
            self._finish_round("given_up", False)
        self.destroy()

    def _on_stats(self) -> None:
        """Open the modal Stats window.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self._stats_window = StatsWindow(self)

    def _on_how_to_play(self) -> None:
        """Open the modal, read-only How to Play window (SPEC §7.7).

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        window = tk.Toplevel(self)
        window.title("How to Play")
        window.resizable(False, False)
        window.transient(self)
        tk.Label(window, text="How to Play").pack(pady=(10, 5))
        tk.Label(
            window, text=self.HOW_TO_PLAY_TEXT, justify=tk.LEFT
        ).pack(padx=10, pady=5)
        tk.Button(window, text="Close", command=window.destroy).pack(
            pady=(5, 10)
        )
        window.grab_set()
