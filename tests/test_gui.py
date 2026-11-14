import tkinter as tk
from collections.abc import Iterator
from typing import Any

import pytest

import krypto.gui as gui_module
from krypto.gui import KryptoApp

TARGET: int = 17
HAND: list[int] = [3, 5, 8, 12, 21]
BUTTON_NAMES: tuple[str, ...] = (
    "how_to_play",
    "stats",
    "hand_0",
    "hand_1",
    "hand_2",
    "hand_3",
    "hand_4",
    "open_paren",
    "close_paren",
    "clear",
    "undo",
    "submit",
    "give_up",
    "start_new_game",
    "exit",
)


class FakeClock:
    """Deterministic stand-in for the time module's monotonic clock."""

    def __init__(self) -> None:
        """Start the fake clock at 100.0 seconds.

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
        self.now: float = 100.0

    def monotonic(self) -> float:
        """Return the current fake time.

        Parameters
        ----------
        None

        Returns
        -------
        float
            The current fake time in seconds.

        Raises
        ------
        None
        """
        return self.now


class FakeMessageBox:
    """Stand-in for tkinter.messagebox that records calls."""

    def __init__(self) -> None:
        """Create a box that confirms every question by default.

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
        self.confirm: bool = True
        self.questions: list[str] = []
        self.errors: list[tuple[str, str]] = []

    def askyesno(
        self, title: str, message: str, parent: Any = None
    ) -> bool:
        """Record a Yes/No question and return the configured answer.

        Parameters
        ----------
        title : str
            The dialog title.
        message : str
            The dialog message.
        parent : Any, optional
            The parent window, ignored.

        Returns
        -------
        bool
            The configured confirmation answer.

        Raises
        ------
        None
        """
        self.questions.append(title)
        return self.confirm

    def showerror(
        self, title: str, message: str, parent: Any = None
    ) -> None:
        """Record an error dialog.

        Parameters
        ----------
        title : str
            The dialog title.
        message : str
            The dialog message.
        parent : Any, optional
            The parent window, ignored.

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.errors.append((title, message))


def _controls(**enabled: bool) -> dict[str, bool]:
    """Build a full controls dict with every control disabled by default.

    Parameters
    ----------
    **enabled : bool
        Control names mapped to their enabled state.

    Returns
    -------
    dict[str, bool]
        Every button name and "op", mapped to an enabled flag.

    Raises
    ------
    None
    """
    controls = {name: False for name in (*BUTTON_NAMES, "op")}
    controls.update(enabled)
    return controls


def _state(app: KryptoApp, name: str) -> str:
    """Return the Tk state string of a named button.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    name : str
        A key in app._buttons.

    Returns
    -------
    str
        "normal" or "disabled".

    Raises
    ------
    None
    """
    return str(app._buttons[name].cget("state"))


def _start(app: KryptoApp) -> None:
    """Start a new round on the given app.

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    app._on_start_new_game()


def _set_evaluate(
    monkeypatch: pytest.MonkeyPatch, result: tuple[bool, bool, Any]
) -> None:
    """Replace evaluate() in the gui module with a fixed result.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.
    result : tuple[bool, bool, Any]
        The (is_valid, is_win, value) tuple to return.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    monkeypatch.setattr(
        gui_module, "evaluate", lambda tokens, hand, target: result
    )


@pytest.fixture
def clock(monkeypatch: pytest.MonkeyPatch) -> FakeClock:
    """Replace the time module used by the gui module with a fake clock.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.

    Returns
    -------
    FakeClock
        The fake clock installed in the gui module.

    Raises
    ------
    None
    """
    fake = FakeClock()
    monkeypatch.setattr(gui_module, "time", fake)
    return fake


@pytest.fixture
def results(monkeypatch: pytest.MonkeyPatch) -> list[tuple[Any, ...]]:
    """Replace append_result() with a recorder so no history is written.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.

    Returns
    -------
    list[tuple[Any, ...]]
        One tuple per recorded call: (target, hand, is_win, cards_used,
        time_sec).

    Raises
    ------
    None
    """
    calls: list[tuple[Any, ...]] = []

    def fake_append(
        target: int,
        hand: list[int],
        is_win: bool,
        cards_used: int,
        time_sec: float,
    ) -> None:
        calls.append((target, list(hand), is_win, cards_used, time_sec))

    monkeypatch.setattr(gui_module, "append_result", fake_append)
    return calls


@pytest.fixture
def dialogs(monkeypatch: pytest.MonkeyPatch) -> FakeMessageBox:
    """Replace the messagebox module used by the gui module.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.

    Returns
    -------
    FakeMessageBox
        The fake message box installed in the gui module.

    Raises
    ------
    None
    """
    box = FakeMessageBox()
    monkeypatch.setattr(gui_module, "messagebox", box)
    return box


@pytest.fixture
def app(
    monkeypatch: pytest.MonkeyPatch,
    clock: FakeClock,
    results: list[tuple[Any, ...]],
    dialogs: FakeMessageBox,
) -> Iterator[KryptoApp]:
    """Create a KryptoApp with deterministic deal and isolated side effects.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.
    clock : FakeClock
        The fake clock.
    results : list[tuple[Any, ...]]
        The append_result() recorder.
    dialogs : FakeMessageBox
        The fake message box.

    Yields
    ------
    KryptoApp
        A fresh application instance.

    Raises
    ------
    None
        Skips the test if no display is available.
    """
    monkeypatch.setattr(
        gui_module, "deal", lambda *args, **kwargs: (TARGET, list(HAND))
    )
    try:
        instance = KryptoApp()
    except tk.TclError:
        pytest.skip("No display available for Tkinter")
    yield instance
    try:
        if instance._timer_job is not None:
            instance.after_cancel(instance._timer_job)
        instance.destroy()
    except tk.TclError:
        pass


def test_initial_state(app: KryptoApp) -> None:
    """A new app starts not_started with placeholder labels.

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    assert app._round_state == "not_started"
    assert app._target_var.get() == "Target: -"
    assert app._time_var.get() == "Time: 00:00.0"
    assert app._tokens == []


def test_start_new_game_deals_round(app: KryptoApp) -> None:
    """Start New Game stores the deal and shows it on screen.

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    assert app._round_state == "in_progress"
    assert app._target == TARGET
    assert app._hand == HAND
    assert app._target_var.get() == f"Target: {TARGET}"
    for index, card in enumerate(HAND):
        assert app._buttons[f"hand_{index}"].cget("text") == str(card)
    assert app._time_var.get() == "Time: 00:00.0"


def test_start_new_game_clears_previous_tokens(app: KryptoApp) -> None:
    """Starting a new round empties any leftover tokens.

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    app._on_hand_click(0)
    _start(app)
    assert app._tokens == []


def test_hand_click_appends_index(app: KryptoApp) -> None:
    """Clicking a hand card appends its index to the token list.

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    app._on_hand_click(2)
    assert app._tokens == [2]


def test_symbol_click_appends_symbol(app: KryptoApp) -> None:
    """Clicking an operator or parenthesis appends that symbol.

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    app._on_symbol_click("(")
    app._on_symbol_click("*")
    assert app._tokens == ["(", "*"]


def test_undo_removes_last_token(app: KryptoApp) -> None:
    """Undo removes only the most recently placed token.

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    app._on_hand_click(0)
    app._on_symbol_click("+")
    app._on_undo()
    assert app._tokens == [0]


def test_undo_on_empty_expression_is_noop(app: KryptoApp) -> None:
    """Undo with no tokens leaves the expression empty without error.

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    app._on_undo()
    assert app._tokens == []


def test_clear_empties_expression(app: KryptoApp) -> None:
    """Clear removes every token.

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    app._on_hand_click(0)
    app._on_symbol_click("-")
    app._on_hand_click(1)
    app._on_clear()
    assert app._tokens == []
    assert app._expr_var.get() == ""


def test_expression_display_matches_build_expr_string(app: KryptoApp) -> None:
    """The expression label shows the output of build_expr_string().

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    app._on_hand_click(0)
    app._on_symbol_click("+")
    app._on_hand_click(1)
    expected = gui_module.build_expr_string(app._tokens, app._hand)
    assert app._expr_var.get() == expected


def test_refresh_controls_applies_returned_states(
    app: KryptoApp, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Buttons take their state from get_available_controls().

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    enabled = {"hand_0": True, "submit": True, "op": True}
    monkeypatch.setattr(
        gui_module,
        "get_available_controls",
        lambda state, tokens: _controls(**enabled),
    )
    app._refresh_controls()
    assert _state(app, "hand_0") == "normal"
    assert _state(app, "hand_1") == "disabled"
    assert _state(app, "submit") == "normal"
    for button in app._op_buttons:
        assert str(button.cget("state")) == "normal"


def test_real_controls_disable_start_and_stats_in_progress(
    app: KryptoApp,
) -> None:
    """During a round, Start New Game and Stats are unavailable.

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    assert _state(app, "start_new_game") == "disabled"
    assert _state(app, "stats") == "disabled"


def test_update_timer_display_formats_time(app: KryptoApp) -> None:
    """The stopwatch label uses the MM:SS.t format.

    Parameters
    ----------
    app : KryptoApp
        The application under test.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    app._update_timer_display(42.7)
    assert app._time_var.get() == "Time: 00:42.7"
    app._update_timer_display(75.0)
    assert app._time_var.get() == "Time: 01:15.0"
    app._update_timer_display(600.5)
    assert app._time_var.get() == "Time: 10:00.5"


def test_tick_updates_display_and_reschedules(
    app: KryptoApp, clock: FakeClock
) -> None:
    """A tick refreshes the stopwatch and schedules the next tick.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    clock : FakeClock
        The fake clock.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    clock.now = 103.5
    app._tick()
    assert app._time_var.get() == "Time: 00:03.5"
    assert app._timer_job is not None
    app.after_cancel(app._timer_job)


def test_submit_invalid_expression_keeps_round(
    app: KryptoApp, monkeypatch: pytest.MonkeyPatch, results: list
) -> None:
    """An invalid expression shows an error and changes nothing else.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.
    results : list
        The append_result() recorder.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    app._on_symbol_click("+")
    _set_evaluate(monkeypatch, (False, False, None))
    app._on_submit()
    assert "Invalid expression" in app._status_var.get()
    assert app._round_state == "in_progress"
    assert app._tokens == ["+"]
    assert results == []


def test_submit_wrong_result_shows_value(
    app: KryptoApp, monkeypatch: pytest.MonkeyPatch, results: list
) -> None:
    """A wrong result is reported with the value the expression produced.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.
    results : list
        The append_result() recorder.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    app._on_hand_click(0)
    _set_evaluate(monkeypatch, (True, False, 14))
    app._on_submit()
    status = app._status_var.get()
    assert "14" in status
    assert str(TARGET) in status
    assert app._round_state == "in_progress"
    assert results == []


def test_submit_win_records_result_and_freezes_timer(
    app: KryptoApp,
    clock: FakeClock,
    monkeypatch: pytest.MonkeyPatch,
    results: list[tuple[Any, ...]],
) -> None:
    """A correct submit records the win and stops the stopwatch.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    clock : FakeClock
        The fake clock.
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.
    results : list[tuple[Any, ...]]
        The append_result() recorder.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    app._on_hand_click(0)
    app._on_symbol_click("+")
    app._on_hand_click(1)
    _set_evaluate(monkeypatch, (True, True, 17))
    clock.now = 142.7
    app._on_submit()
    assert len(results) == 1
    target, hand, is_win, cards_used, time_sec = results[0]
    assert (target, hand, is_win, cards_used) == (TARGET, HAND, True, 2)
    assert time_sec == pytest.approx(42.7)
    assert app._round_state == "won"
    assert app._timer_job is None
    assert "2 cards" in app._status_var.get()


def test_win_score_counts_only_hand_cards(
    app: KryptoApp,
    monkeypatch: pytest.MonkeyPatch,
    results: list[tuple[Any, ...]],
) -> None:
    """Operators and parentheses do not count toward the score.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.
    results : list[tuple[Any, ...]]
        The append_result() recorder.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    for token in ["(", 0, "+", 1, ")", "*", 2]:
        if isinstance(token, int):
            app._on_hand_click(token)
        else:
            app._on_symbol_click(token)
    _set_evaluate(monkeypatch, (True, True, 17))
    app._on_submit()
    assert results[0][3] == 3


def test_give_up_confirmed_records_zero_score(
    app: KryptoApp,
    dialogs: FakeMessageBox,
    results: list[tuple[Any, ...]],
) -> None:
    """A confirmed Give Up records a zero-score loss and freezes the round.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    dialogs : FakeMessageBox
        The fake message box.
    results : list[tuple[Any, ...]]
        The append_result() recorder.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    app._on_hand_click(0)
    dialogs.confirm = True
    app._on_give_up()
    assert len(results) == 1
    target, hand, is_win, cards_used, _ = results[0]
    assert (target, hand, is_win, cards_used) == (TARGET, HAND, False, 0)
    assert app._round_state == "given_up"
    assert app._timer_job is None


def test_give_up_declined_changes_nothing(
    app: KryptoApp,
    dialogs: FakeMessageBox,
    results: list[tuple[Any, ...]],
) -> None:
    """Declining Give Up leaves the round untouched.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    dialogs : FakeMessageBox
        The fake message box.
    results : list[tuple[Any, ...]]
        The append_result() recorder.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    dialogs.confirm = False
    app._on_give_up()
    assert results == []
    assert app._round_state == "in_progress"
    app.after_cancel(app._timer_job)


def test_exit_not_started_closes_without_recording(
    app: KryptoApp,
    dialogs: FakeMessageBox,
    results: list[tuple[Any, ...]],
) -> None:
    """Exit outside a round closes immediately with no record or prompt.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    dialogs : FakeMessageBox
        The fake message box.
    results : list[tuple[Any, ...]]
        The append_result() recorder.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    app._on_exit()
    assert results == []
    assert dialogs.questions == []


def test_exit_in_progress_confirmed_records_and_closes(
    app: KryptoApp,
    dialogs: FakeMessageBox,
    results: list[tuple[Any, ...]],
) -> None:
    """A confirmed Exit mid-round records a zero-score give-up.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    dialogs : FakeMessageBox
        The fake message box.
    results : list[tuple[Any, ...]]
        The append_result() recorder.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    dialogs.confirm = True
    app._on_exit()
    assert dialogs.questions == ["Exit"]
    assert len(results) == 1
    assert results[0][2:4] == (False, 0)


def test_exit_in_progress_declined_keeps_round(
    app: KryptoApp,
    dialogs: FakeMessageBox,
    results: list[tuple[Any, ...]],
) -> None:
    """Declining Exit mid-round keeps the round running.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    dialogs : FakeMessageBox
        The fake message box.
    results : list[tuple[Any, ...]]
        The append_result() recorder.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    dialogs.confirm = False
    app._on_exit()
    assert results == []
    assert app._round_state == "in_progress"
    assert app.winfo_exists()
    app.after_cancel(app._timer_job)


def test_window_close_button_behaves_like_exit(
    app: KryptoApp,
    dialogs: FakeMessageBox,
    results: list[tuple[Any, ...]],
) -> None:
    """The WM_DELETE_WINDOW handler runs the same logic as Exit.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    dialogs : FakeMessageBox
        The fake message box.
    results : list[tuple[Any, ...]]
        The append_result() recorder.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    _start(app)
    dialogs.confirm = False
    command = app.protocol("WM_DELETE_WINDOW")
    app.tk.call(command)
    assert results == []
    assert app._round_state == "in_progress"
    app.after_cancel(app._timer_job)


def test_save_failure_shows_error_and_still_concludes(
    app: KryptoApp,
    monkeypatch: pytest.MonkeyPatch,
    dialogs: FakeMessageBox,
) -> None:
    """An OSError while saving is shown to the player, not raised.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.
    dialogs : FakeMessageBox
        The fake message box.

    Returns
    -------
    None

    Raises
    ------
    None
    """

    def failing_append(*args: Any, **kwargs: Any) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(gui_module, "append_result", failing_append)
    _start(app)
    dialogs.confirm = True
    app._on_give_up()
    assert len(dialogs.errors) == 1
    assert app._round_state == "given_up"


def test_stats_opens_stats_window(
    app: KryptoApp, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The Stats button opens a StatsWindow parented to the app.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    opened: list[Any] = []

    class FakeStatsWindow:
        def __init__(self, parent: Any) -> None:
            opened.append(parent)

    monkeypatch.setattr(gui_module, "StatsWindow", FakeStatsWindow)
    app._on_stats()
    assert opened == [app]


def test_how_to_play_opens_modal_window(
    app: KryptoApp, monkeypatch: pytest.MonkeyPatch
) -> None:
    """How to Play opens a titled window containing the rules text.

    Parameters
    ----------
    app : KryptoApp
        The application under test.
    monkeypatch : pytest.MonkeyPatch
        The pytest monkeypatch fixture.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    monkeypatch.setattr(tk.Toplevel, "grab_set", lambda self: None)
    app._on_how_to_play()
    windows = [w for w in app.winfo_children() if isinstance(w, tk.Toplevel)]
    assert len(windows) == 1
    window = windows[0]
    assert window.title() == "How to Play"
    labels = [
        str(w.cget("text"))
        for w in window.winfo_children()
        if isinstance(w, tk.Label)
    ]
    assert KryptoApp.HOW_TO_PLAY_TEXT in labels
    window.destroy()
