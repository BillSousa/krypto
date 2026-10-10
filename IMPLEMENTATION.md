# Krypto — Python Implementation Notes

Companion to `SPEC.md`. `SPEC.md` defines what the game does and how it
behaves; this file covers how it gets built.

## Minimum Supported Python Version
>=3.11

## Module Strategy
Small, single-responsibility modules. One function or class per file.
Test files should mirror source files 1:1.

## Packaging
- Packaging: PyInstaller, producing a Windows `.exe` and a Linux binary
  (built on Linux), both reading the same history file from a shared folder.

## Project layout
```
src/
  krypto/
    __init__.py
    build_deck.py
    deal.py
    build_expr_string.py
    is_valid_expr_str.py
    evaluate.py
    get_history_path.py
    append_result.py
    load_history.py
    derive_stats.py
    derive_best_times.py
    get_available_controls.py
    gui.py
    stats_window.py
    main.py
tests/
  test_build_deck.py
  test_deal.py
  test_build_expr_string.py
  test_is_valid_expr_str.py
  test_evaluate.py
  test_get_history_path.py
  test_append_result.py
  test_load_history.py
  test_derive_stats.py
  test_derive_best_times.py
  test_get_available_controls.py
  test_gui.py
  test_stats_window.py
  test_main.py
  test_integration_append_load.py
  test_integration_deal_build_evaluate.py
  test_integration_load_derive.py
```

## Module Breakdown
Each file below holds exactly one function (or, for `gui.py` and
`stats_window.py`, one class). All function modules are stateless
functions — no classes.

### build_deck.py
`build_deck.py` holds a single function, `build_deck() -> list[int]`,
and it's the only place the 56-card composition lives in code. It
takes no arguments and returns a fresh 56-item list, unshuffled, in
ascending order, built from the exact counts in SPEC §3 (1–6 three
times each, 7–10 four times each, 11–17 twice each, 18–25 once each) —
never a random or partial deck.
```python
def build_deck() -> list[int]:
    """Build the standard 56-card Krypto deck.

    Returns
    -------
    list[int]
        A fresh 56-item list, unshuffled, in ascending order. Built
        from SPEC §3's exact counts: values 1-6 appear 3 times each,
        7-10 appear 4 times each, 11-17 appear 2 times each, and
        18-25 appear 1 time each.

    Raises
    ------
    None
    """
    deck: list[int] = []

    for value in range(1, 7):
        deck.extend([value] * 3)

    for value in range(7, 11):
        deck.extend([value] * 4)

    for value in range(11, 18):
        deck.extend([value] * 2)

    for value in range(18, 26):
        deck.extend([value] * 1)

    return deck
```

### deal.py
`deal.py` holds a single function, `deal(rng: random.Random | None =
None) -> tuple[int, list[int]]`, and it's the only place a round's
cards get chosen. First, it imports `build_deck` from `build_deck.py`.
Second, it shuffles a fresh copy of the 56-card list provided by 
`build_deck`. Shuffling uses `rng` if it is passed, so tests can pass 
a seeded `random.Random` for repeatable deals. If `rng` is not passed, 
which is the case in normal game-play, then an unseeded `random.Random` 
is used. Third, six cards are drawn from the shuffled deck. The first 
card drawn as `target`, the next five as `hand`, in that drawn order.
`target` is a plain `int`; `hand` is a `list[int]` of length 5, in
dealt order. There is no dedicated `Card` class — cards have no 
identity beyond their position in the hand list, so a plain `int` 
addressed by index is sufficient. Finally, `(target, hand)` is returned.
```python
import random

from krypto.build_deck import build_deck


def deal(
    rng: random.Random | None = None,
) -> tuple[int, list[int]]:
    """Deal one Krypto round: a target card and a 5-card hand.

    Parameters
    ----------
    rng : random.Random, optional
        A seeded random source for deterministic, repeatable deals
        (used by tests). If None, a fresh unseeded random.Random() is
        used.

    Returns
    -------
    tuple[int, list[int]]
        (target, hand) — the first card drawn as target, the next
        five as hand, in that drawn order. hand has length 5.

    Raises
    ------
    None
    """
    if rng is None:
        rng = random.Random()

    deck = build_deck()
    rng.shuffle(deck)

    target = deck[0]
    hand = deck[1:6]

    return target, hand
```

### build_expr_string.py
`build_expr_string.py` holds a single function,
`build_expr_string(tokens: list[int | str], hand: list[int]) -> str`,
and it's the only place the clicked token list turns into a plain
expression string. Each token is either an `int` (an index into
`hand`, meaning "this hand card was clicked") or a `str` (one of
`+ - * / ( )`, meaning "this symbol was clicked"). For an `int` token
it looks up `hand[token]` and appends that number's digits; for a
`str` token it appends the symbol as-is. Returns a plain string (e.g.
`"(3+5)*2"`) — digits only, never `Fraction()`-wrapped, since that
wrapping is `evaluate.py`'s job, not this file's.
```python
   <<<function signature>>>
   <<<docstring>>>
   <<<code body>>>
```

### is_valid_expr_str.py
`is_valid_expr_str.py` holds a single function,
`is_valid_expr_str(expr_str: str) -> bool`, and it's the only place
expr_str validation rules live — separate from `evaluate.py` so that
new rules discovered later can be added here without touching
`evaluate.py` or `test_evaluate.py`. `evaluate()` calls it first and
returns `(False, False, None)` immediately, without calling `eval()`
at all, if it returns `False`. Currently rejects: an empty string, and
any two adjacent characters from `+-*/` (e.g. `"3++5"`, `"3--5"`,
`"3**5"`, `"3//5"`) — Python's `eval()` would otherwise silently accept
these as unary plus/minus or as the exponent/floor-division operators,
producing a wrong result instead of failing, since a mis-click or
double-click on an operator button isn't prevented by any live
validation (SPEC §4).
```python
import re


def is_valid_expr_str(expr_str: str) -> bool:
    """Check whether an expression string is well-formed enough to
    attempt evaluation.

    Parameters
    ----------
    expr_str : str
        The clicked expression, exactly as built (e.g. "(3+5)*2").

    Returns
    -------
    bool
        False if expr_str is empty, or contains two or more adjacent
        characters from "+-*/" (e.g. "3++5", "3--5", "3**5", "3//5")
        — sequences Python's eval() would otherwise silently accept as
        unary plus/minus, or as the exponent/floor-division operators,
        instead of rejecting as malformed. True otherwise. This does
        not guarantee expr_str is fully valid Python syntax (e.g.
        unbalanced parentheses are not checked here); it only catches
        cases eval() would not raise on by itself. Any other malformed
        case is still caught by evaluate()'s own try/except around
        eval().

    Raises
    ------
    None
    """
    if not expr_str:
        return False

    if re.search(r"[+\-*/]{2,}", expr_str):
        return False

    return True
```

### evaluate.py
`evaluate.py` holds a single function, `evaluate(expr_str: str, target:
int)`, and it is the one place in the codebase that turns a completed
expression into a pass/fail/wrong-answer result — it owns the entire
win-check, not just the arithmetic. It calls `is_valid_expr_str()` from
`is_valid_expr_str.py` first; if that returns `False`, it returns
`(False, False, None)` immediately without calling `eval()`.
```python
import re
from fractions import Fraction

from krypto.is_valid_expr_str import is_valid_expr_str


def evaluate(
    expr_str: str, target: int
) -> tuple[bool, bool, Fraction | None]:
    """Evaluate an expression string and check it against the target.

    `expr_str` is a plain string exactly as the digits, operators, and
    parentheses were clicked (e.g. "3+5*2" or "(3+5)*2") — never
    Fraction()-wrapped by the caller, since that wrapping is
    evaluate()'s own job, not gui.py's (gui.py is not permitted to
    contain evaluation logic). Internally, evaluate() rewrites every
    number in expr_str as Fraction(<value>) before calling Python's
    eval() with an empty __builtins__ dict, so the whole computation
    happens over exact rationals rather than floats, and a genuine
    divide-by-zero raises a catchable ZeroDivisionError instead of
    producing inf or nan. expr_str is checked with is_valid_expr_str()
    first (empty string, adjacent operators) and treated as invalid
    immediately, without attempting to eval() it at all, if that check
    fails. Any exception raised during the rewrite or the eval() call —
    SyntaxError, ZeroDivisionError, TypeError, or anything else — is
    caught and treated as an invalid expression, never allowed to
    propagate to the caller.

    Parameters
    ----------
    expr_str : str
        The clicked expression, exactly as built (e.g. "(3+5)*2").
        Never pre-wrapped in Fraction() by the caller.
    target : int
        The round's target number to check the result against.

    Returns
    -------
    tuple[bool, bool, Fraction | None]
        A three-item tuple: ``(is_valid, is_win, value)``.

        - ``is_valid`` is False only when the expression could not be
          computed at all (empty string, unbalanced parens, trailing
          operator, division by zero, etc.), in which case ``value``
          is None and ``is_win`` is always False.
        - Whenever ``is_valid`` is True, ``value`` holds the exact
          Fraction the expression computed — even when it doesn't
          match the target — because the caller needs to show the
          player what their expression actually evaluated to on a
          wrong-answer Submit (SPEC §7.3), not just a bare failure
          message.
        - ``is_win`` is True only when ``is_valid`` is True and
          ``value == Fraction(target)`` exactly. Comparing to target
          lives inside evaluate(), not gui.py, because a win check is
          evaluation logic, not presentation.

    Raises
    ------
    None
        All exceptions raised while parsing or evaluating expr_str are
        caught internally and reported through the return value, never
        propagated to the caller.

    Notes
    -----
    evaluate() does not compute cards_used/score — it only sees the
    flattened text and has no way to tell which digits came from which
    hand-card button, so that has to be derived elsewhere, from the
    token list, not from this string.
    """
    if not is_valid_expr_str(expr_str):
        return False, False, None

    wrapped = re.sub(r"\d+", lambda m: f"Fraction({m.group()})", expr_str)

    try:
        value = eval(
            wrapped, {"__builtins__": {}}, {"Fraction": Fraction}
        )
    except Exception:
        # Deliberately broad: SyntaxError, ZeroDivisionError,
        # TypeError, and anything else all mean "invalid expression."
        return False, False, None

    is_win = value == Fraction(target)
    return True, is_win, value
```

### get_history_path.py
`get_history_path.py` holds a single function, `get_history_path() ->
Path`, and it's the only place the history file's location is decided.
`append_result.py` and `load_history.py` both call `get_history_path()` 
rather than building the path themselves. It returns the path to 
`krypto_history.txt` which should be in the same directory as the 
krypto game executable. When frozen by PyInstaller, that's
`Path(sys.executable).parent`; when run as a plain script that's,
`Path(__file__).resolve().parent`. The function never hardcodes a
shared path; it always resolves to wherever the executable sits. The
Windows `.exe` and Linux binary end up reading the same file only if
both are in the same folder, which is expected, not enforced in code.
```python
   <<<function signature>>>
   <<<docstring>>>
   <<<code body>>>
```

### append_result.py
`append_result.py` holds a single function, `append_result(target: int,
hand: list[int], is_win: bool, cards_used: int, time_sec: float)`, and
it's the only place that writes a completed round to the history file.
It calls `get_history_path()` from `get_history_path.py` to find where
to write. It builds the timestamp itself (current time, ISO 8601),
formats one line to match the example directly below, and appends it —
it never overwrites or rewrites existing lines. It opens the file in
append mode, which creates `krypto_history.txt` automatically the
first time it's called if the file doesn't already exist next to the
executable — no separate creation step needed.

Plain text, append-only, one line per concluded round:
```
<ISO8601 timestamp>  target=<int>  hand=<c1,c2,c3,c4,c5>  result=<WIN|GIVEUP>  cards_used=<int>  time_sec=<float>
```
Example:
```
2026-09-27T14:32:05  target=17  hand=3,5,8,12,21  result=WIN     cards_used=4  time_sec=42.7
2026-09-27T14:35:10  target=9   hand=1,2,7,15,19  result=GIVEUP  cards_used=0  time_sec=118.3
```
```python
   <<<function signature>>>
   <<<docstring>>>
   <<<code body>>>
```

### load_history.py
`load_history.py` holds a single function, `load_history() ->
list[dict]`, and it's the only place the history file gets read 
back. It takes no arguments, calls `get_history_path()` from
`get_history_path.py` to find the file, and returns one dict per
successfully parsed line. The keys of the dicts are `timestamp`, 
`target`, `hand`, `is_win`, `cards_used`, `time_sec`. The history 
file's `WIN`/`GIVEUP` text is converted back into a bool to match 
`append_result.py`'s own `is_win` parameter. The history file's 
comma-separated `hand` text is split back into `list[int]`, 
matching `append_result.py`'s own `hand` parameter. If the history 
file doesn't exist yet, an empty list is returned rather than 
raising an exception (SPEC §6: no history file means zero games
played, not an error). Each line is parsed independently inside its
own `try/except`; a line that fails to parse is skipped, not fatal 
to the rest of the scan.
```python
   <<<function signature>>>
   <<<docstring>>>
   <<<code body>>>
```

### derive_stats.py
`derive_stats.py` holds a single function, `derive_stats(history:
list[dict]) -> dict`, and it's the only place the top half of the
Stats screen (§7.5) gets computed — everything except the Top 10
table, which is the job of `derive_best_times.py`. It takes the list 
of records from `load_history()` (it doesn't read the history file 
itself) and returns a dict with `score_counts`, `total_games`, 
`average_score`, and `average_time_5_card`. `score_counts` is a 0–5 
breakdown, where a give-up counts as score 0 and a win's score is 
its `cards_used`. `total_games` is the record count. `average_score` 
is the mean of `cards_used` across every record, with give-ups 
included as 0. `average_time_5_card` is the mean `time_sec` across 
only the wins where `cards_used == 5`.

```python
   <<<function signature>>>
   <<<docstring>>>
   <<<code body>>>
```

### derive_best_times.py
`derive_best_times.py` holds a single function,
`derive_best_times(history: list[dict]) -> list[dict]`, and it's the
only place the Top 10 table on the Stats screen (§7.5) gets computed.
It takes the list of records from `load_history()`, which is the same 
input as `derive_stats()`; the history is not re-read from file here.
The history is filtered to only the wins where `cards_used == 5`, 
sorts them by `time_sec` ascending, and returns the fastest 10 as a 
list of dicts. The dicts' keys are `timestamp`, `target`, `hand` (as 
`list[int]`, unchanged from `load_history()`), and `time_sec` — the 
exact columns the table displays. If fewer than 10 qualifying wins 
exist, it returns however many there are, not padded to 10.
```python
   <<<function signature>>>
   <<<docstring>>>
   <<<code body>>>
```

### get_available_controls.py
`get_available_controls.py` holds a single function,
`get_available_controls(round_state: str, tokens: list[int | str]) ->
dict`, and it's the only place SPEC §7.2's availability table gets
decided — availability is never inferred ad hoc inside `gui.py`. 
It takes the current round state (`"not_started"`, `"in_progress"`, 
`"won"`, or `"given_up"`) and the ordered token list `gui.py` has 
built so far, and returns a dict of booleans keyed by control name. 
The ordered token list from `gui.py` contains `int` hand indices or 
`str` symbols — see `build_expr_string.py`. The keys of the dict of 
booleans are `hand_0`–`hand_4`, `op`, `open_paren`, `close_paren`,
`undo`, `clear`, `submit`, `give_up`, `start_new_game`, `stats`,
and `exit`. `gui.py` just applies each value from this dict to the 
matching button, it doesn't compute any of them itself.
```python
   <<<function signature>>>
   <<<docstring>>>
   <<<code body>>>
```

### gui.py
`gui.py` holds a single class, `KryptoApp` — the only class besides 
`StatsWindow` in the project — and it's the top-level Tkinter 
application. It is built with plain Tkinter (stdlib) and default/plain 
styling, no theming. `KryptoApp` extends `tk.Tk` (or wraps a `tk.Tk` 
instance), so it has a `.mainloop()` method inherited from Tkinter 
itself. `.mainloop()` is Tkinter's event loop: it keeps the window 
open, waits for clicks, and dispatches them to the right callback. 
It's called once, from `main.py`, and blocks until the window is closed 
(Exit, or the OS window-close button). `KryptoApp` owns the round state
(`"not_started"`/`"in_progress"`/`"won"`/`"given_up"`), the current
`target`/`hand`, and the ordered token list, and creates every widget
from the Game Layout diagram below. It formats the timer display and 
result messages itself (§7.3) — everything else is delegated to the 
functions above. 
It starts in `"not_started"` on launch (SPEC §7.2) — no deal happens 
until Start New Game is clicked. When Start New Game is clicked, it 
calls `deal()` from `deal.py` to get a fresh `(target, hand)`, clears 
the token list, and records `start_time = time.monotonic()`, then begins 
a recurring `.after()` call that updates the displayed timer while in 
progress. Its token list holds items that are each either an `int` 
(the index of a clicked hand card, into `hand`) or a `str` (one of 
`+ - * / ( )`, a clicked symbol) — see `build_expr_string.py`. 
On each state or token change it calls `get_available_controls()` 
and applies the result to the buttons. Clicking a hand card appends 
its index to the token list and disables the card in the gui. Undo 
re-enables that hand button if the popped token is an `int`. Submit 
calls `build_expr_string()` then `evaluate()`, and on a win calls 
`append_result()`. Give Up and Exit ask for confirmation, then call 
`append_result()` the same way, with Exit closing the window afterward. 
On Submit-success, confirmed Give Up, or confirmed Exit, it computes 
`time_sec = time.monotonic() - start_time` and passes that to 
`append_result()`. Stats opens a `StatsWindow`.

Game layout (SPEC §7.1):
```
+----------------------------------------------------------+
|  Krypto                                          [Stats] |
+----------------------------------------------------------+
|   Target: 17                        Time: 00:42.7        |
+----------------------------------------------------------+
|   Hand:   [ 3 ] [ 5 ] [ 8 ] [ 12 ] [ 21 ]                 |
+----------------------------------------------------------+
|   Ops:    [ + ] [ - ] [ * ] [ / ]   [ ( ]  [ ) ]          |
+----------------------------------------------------------+
|   Expr:  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]    |
+----------------------------------------------------------+
|   [Clear]      [Undo]      [Submit]      [Give Up]       |
|                                                           |
|   (status message line — result/errors appear here)       |
+----------------------------------------------------------+
|              [ Start New Game ] [ Exit ]                 |
+----------------------------------------------------------+
```

```python
   <<<class>>>
   <<<docstring>>>
   <<<code body>>>
```

### stats_window.py
`stats_window.py` holds a single class, `StatsWindow`, built with
plain Tkinter (stdlib) and default/plain styling, no theming. It's
the only place the Stats screen (§7.5) is built and shown. It owns 
only its own window and Close button; it never touches `KryptoApp`'s 
state or pauses the active round's timer. It's opened by `gui.py`'s 
Stats button and takes no game state from `KryptoApp` at 
construction time — instead it builds the Stats screen from the 
history file, if it exists. This is done by calling `load_history()`, 
`derive_stats()`, and `derive_best_times()` to get fresh numbers every 
time it opens, per §7.4. Each best-time record's `hand` comes in as 
`list[int]` (from `load_history()`, via `derive_best_times()`); 
`stats_window.py` joins it into a comma-separated string (e.g. 
`"1,3,6,12,21"`) for the table — this formatting is the only place 
it happens, and it stays `list[int]` everywhere upstream.

Stats layout (SPEC §7.5):
```
+----------------------------------------------------------+
|                         Stats                             |
+----------------------------------------------------------+
|   Final Score                                Count        |
+----------------------------------------------------------+
|   0                                           235         |
+----------------------------------------------------------+
|   1                                           498         |
+----------------------------------------------------------+
|   2                                          1038         |
+----------------------------------------------------------+
|   3                                          2842         |
+----------------------------------------------------------+
|   4                                          4234         |
+----------------------------------------------------------+
|   5                                          8388         |
+----------------------------------------------------------+
|   Total Games Played                        17235         |
+----------------------------------------------------------+
|   Average Final Score                       4.060         |
+----------------------------------------------------------+
|   Average Time (5 card wins only)          63.345 sec     |
+----------------------------------------------------------+
|   Top 10 Best Times (5 card wins only)                    |
|       Date-Time         Target     Hand      Time (sec)   |
|   2026-05-23T00:00:00     17    1,3,6,12,21     23.5      |
|   2026-08-07T00:00:00     2     3,5,11,15,17    26.7      |
|   2026-04-12T00:00:00     21    10,15,18,22,23  32.7      |
|   2026-07-13T00:00:00     15    2,6,7,22,25     33.1      |
|   2026-05-22T00:00:00     3     1,10,19,22,23   34.3      |
|   2026-05-08T00:00:00     5     2,9,18,21,22    34.6      |
|   2026-06-24T00:00:00     22    3,8,17,20,24    36.1      |
|   2026-01-20T00:00:00     5     4,7,11,19,25    41.8      |
|   2026-03-01T00:00:00     11    5,6,12,18,21    44.3      |
|   2026-04-11T00:00:00     16    6,11,13,17,19   45.5      |
|                                                           |
+----------------------------------------------------------+
|                         [ Close ]                         |
+----------------------------------------------------------+
```
```python
   <<<class>>>
   <<<docstring>>>
   <<<code body>>>
```

### main.py
`main.py` is the entry point — it has no function or class of its own,
just top-level script code guarded by `if __name__ == "__main__":`. It
imports `KryptoApp` from `gui.py`, instantiates it, and calls
`.mainloop()`. Per SPEC §7.2, the app does not deal a round on launch
— it starts with no round in progress, and clicking Start New Game is
what triggers the first deal and starts the timer, same as every round
after. `main.py` itself never calls `deal()`; `KryptoApp` handles that
in response to the button. It has no PyInstaller-specific handling of
its own — that's entirely inside `get_history_path.py`.
```python
   <<<code body>>>
```

## Testing & CI
- `pytest` across all modules.

### test_build_deck.py
```python
from collections import Counter

from krypto.build_deck import build_deck


def test_deck_has_56_cards():
    assert len(build_deck()) == 56


def test_deck_composition_matches_spec():
    counts = Counter(build_deck())
    expected = {}
    for value in range(1, 7):
        expected[value] = 3
    for value in range(7, 11):
        expected[value] = 4
    for value in range(11, 18):
        expected[value] = 2
    for value in range(18, 26):
        expected[value] = 1
    assert counts == expected


def test_deck_is_ascending():
    deck = build_deck()
    assert deck == sorted(deck)


def test_deck_values_in_range_1_to_25():
    deck = build_deck()
    assert all(1 <= value <= 25 for value in deck)


def test_deck_is_not_shuffled_each_call():
    assert build_deck() == build_deck()


def test_deck_calls_return_independent_lists():
    deck_a = build_deck()
    deck_b = build_deck()
    deck_a.append(99)
    assert 99 not in deck_b
```

### test_deal.py
Deterministic via a seeded `random.Random` injected into `deal()`.
```python
import random

from krypto.build_deck import build_deck
from krypto.deal import deal


def test_deal_returns_target_and_hand_of_length_5():
    target, hand = deal(rng=random.Random(42))
    assert isinstance(target, int)
    assert isinstance(hand, list)
    assert len(hand) == 5


def test_deal_values_are_valid_card_values():
    target, hand = deal(rng=random.Random(42))
    assert 1 <= target <= 25
    assert all(1 <= card <= 25 for card in hand)


def test_deal_is_deterministic_with_same_seed():
    target_a, hand_a = deal(rng=random.Random(7))
    target_b, hand_b = deal(rng=random.Random(7))
    assert target_a == target_b
    assert hand_a == hand_b


def test_deal_matches_manual_shuffle_with_same_seed():
    deck = build_deck()
    random.Random(99).shuffle(deck)
    expected_target = deck[0]
    expected_hand = deck[1:6]

    target, hand = deal(rng=random.Random(99))

    assert target == expected_target
    assert hand == expected_hand


def test_deal_without_rng_does_not_raise():
    target, hand = deal()
    assert isinstance(target, int)
    assert len(hand) == 5


def test_deal_different_seeds_can_differ():
    target_a, hand_a = deal(rng=random.Random(1))
    target_b, hand_b = deal(rng=random.Random(2))
    assert (target_a, hand_a) != (target_b, hand_b)
```

### test_build_expr_string.py
```
<<<pytest>>>
```

### test_is_valid_expr_str.py
```python
import pytest

from krypto.is_valid_expr_str import is_valid_expr_str


def test_empty_string_is_invalid():
    assert is_valid_expr_str("") is False


@pytest.mark.parametrize(
    "expr_str",
    [
        "3++5",
        "3--5",
        "3**5",
        "3//5",
        "3+-5",
        "3-*5",
        "((3++5))",
    ],
)
def test_adjacent_operators_are_invalid(expr_str):
    assert is_valid_expr_str(expr_str) is False


@pytest.mark.parametrize(
    "expr_str",
    [
        "3+5",
        "3-5",
        "3*5",
        "3/5",
        "(3+5)*2",
        "(((1+2)*3)-4)+5",
        "12+25",
        "5",
    ],
)
def test_well_formed_expressions_are_valid(expr_str):
    assert is_valid_expr_str(expr_str) is True
```

### test_evaluate.py
```python
from fractions import Fraction

from krypto.evaluate import evaluate


def test_empty_string_is_invalid():
    assert evaluate("", 5) == (False, False, None)


def test_adjacent_operators_is_invalid():
    assert evaluate("3++5", 8) == (False, False, None)


def test_unbalanced_parens_is_invalid():
    is_valid, is_win, value = evaluate("(3+5", 8)
    assert is_valid is False
    assert is_win is False
    assert value is None


def test_division_by_zero_is_invalid():
    is_valid, is_win, value = evaluate("3/0", 3)
    assert is_valid is False
    assert is_win is False
    assert value is None


def test_valid_expression_wrong_answer():
    is_valid, is_win, value = evaluate("3+5", 9)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(8)


def test_valid_expression_correct_answer_is_win():
    is_valid, is_win, value = evaluate("3+5", 8)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(8)


def test_parens_and_precedence():
    is_valid, is_win, value = evaluate("(3+5)*2", 16)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(16)


def test_exact_fraction_arithmetic_no_float_error():
    # 1/3 * 3 must equal exactly 1 with Fraction, unlike float math.
    is_valid, is_win, value = evaluate("1/3*3", 1)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(1)


def test_fractional_result_not_matching_target():
    is_valid, is_win, value = evaluate("1/3", 1)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(1, 3)


def test_negative_intermediate_result_not_matching_target():
    is_valid, is_win, value = evaluate("3-5", 2)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(-2)


def test_single_number_can_win():
    is_valid, is_win, value = evaluate("5", 5)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(5)


def test_max_depth_parens():
    is_valid, is_win, value = evaluate("(((1+2)*3)-4)+5", 10)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(10)
```

### test_get_history_path.py
```
<<<pytest>>>
```

### test_append_result.py
```
<<<pytest>>>
```

### test_load_history.py
```
<<<pytest>>>
```

### test_derive_stats.py
```
<<<pytest>>>
```

### test_derive_best_times.py
```
<<<pytest>>>
```

### test_get_available_controls.py
```
<<<pytest>>>
```

### test_gui.py
GUI tests run headless via a virtual display in CI, e.g.:
```
xvfb-run -a uv run pytest tests/ --doctest-modules -v --maxfail=1 --disable-warnings
```
```
<<<pytest>>>
```

### test_stats_window.py
GUI tests run headless via a virtual display in CI, same as test_gui.py.
```
<<<pytest>>>
```

### test_main.py
```
<<<pytest>>>
```

### test_integration_append_load.py
Writes a record with `append_result()`, reads it back with
`load_history()`, and asserts it matches exactly.
```
<<<pytest>>>
```

### test_integration_deal_build_evaluate.py
Runs the `deal()` → `build_expr_string()` → `evaluate()` pipeline
with a hand-built token list, asserting the result is correct.
```
<<<pytest>>>
```

### test_integration_load_derive.py
Feeds realistic records through `load_history()` into
`derive_stats()`/`derive_best_times()`, asserting the derived numbers
are correct.
```
<<<pytest>>>
```

