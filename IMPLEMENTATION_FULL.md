# Krypto — Python Implementation Notes

Companion to `SPEC_FULL.md`. `SPEC_FULL.md` defines what the game does 
and how it behaves; this file covers how it gets built.

## Explicitly Rejected / Considered-and-Discarded Implementations

Recorded so these don't get re-litigated later:

- **A database for stats/scores** — rejected; a flat history file is
  sufficient for this data shape.
- **Skipping automated tests for the GUI** — rejected; the GUI must be
  tested like everything else.

## Minimum Supported Python Version
>=3.11

## Module Strategy
Small, single-responsibility modules. One function or class per file.
Test files should mirror source files 1:1.

## Packaging
- Packaging: PyInstaller, producing a Linux binary and a Windows `.exe`.
  PyInstaller cannot cross-compile, so each one must be built on its own
  OS: the Linux binary on Linux, and the Windows `.exe` on Windows (a
  Windows machine or a Windows CI runner). Both read the same history
  file from a shared folder.

## Project layout
```
src/
  krypto/
    __init__.py
    build_deck.py
    deal.py
    build_expr_string.py
    is_valid_token_chain.py
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
  test_is_valid_token_chain.py
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
ascending order, built from the exact counts in SPEC §4 (1–6 three
times each, 7–10 four times each, 11–17 twice each, 18–25 once each) —
never a random or partial deck.
```python
def build_deck() -> list[int]:
    """Build the standard 56-card Krypto deck.

    Returns
    -------
    list[int]
        A fresh 56-item list, unshuffled, in ascending order. Built
        from SPEC §4's exact counts: values 1-6 appear 3 times each,
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
expression string. It is called by `evaluate()`, not by `KryptoApp`,
and only after `is_valid_token_chain()` has accepted the token list, so
it does no validation of its own. Each token is either an `int` (an
index into `hand`, meaning "this hand card was clicked") or a `str`
(one of `+ - * / ( )`, meaning "this symbol was clicked"). For an `int`
token it looks up `hand[token]` and appends that number's digits; for a
`str` token it appends the symbol as-is. Returns a plain string (e.g.
`"(3+5)*2"`) — digits only, never `Fraction()`-wrapped, since that
wrapping is `evaluate.py`'s job, not this file's. An `int` token that is 
outside the range of `hand` is a bug in the caller, so build_expr_string() 
is deliberately not under a try/except in `evaluate()`. When an `int` 
token is positive and outside the range of `hand`, `IndexError` is raised.
An `int` token that is negative should not get here because of validation 
in `is_valid_token_chain()`.
```python
   <<<function signature>>>
   <<<docstring>>>
   <<<code body>>>
```

### is_valid_token_chain.py
`is_valid_token_chain.py` holds a single function,
`is_valid_token_chain(tokens: list[int | str]) -> bool`, and it's the
only place token-chain validation rules live — separate from
`evaluate.py` so that new rules discovered later can be added here
without touching `evaluate.py` or `test_evaluate.py`. It checks the
token list itself, before `build_expr_string()` turns it into a string,
because once the tokens are joined into a string the boundaries between
cards are lost. `evaluate()` calls this first and returns
`(False, False, None)` immediately if this returns `False`. 

Currently rejects:
  - an empty list
  - an operator (`+ - * /`) that does not come immediately after a card 
  or a closing parenthesis, meaning an operator at the start or right 
  after an opening parenthesis; Python's `eval()` would otherwise silently 
  accept these as unary plus/minus (e.g. `-3+8`, `(-3+8)`), and a minus 
  created from nothing is not legal Krypto  
  - an operator right after another operator. Python's `eval()` would 
  otherwise silently accept these as unary plus/minus or as the 
  exponent/floor-division operators
  - two cards in a row (two adjacent `int` tokens), which would otherwise 
  be joined into one multi-digit number, e.g. cards 3 and 5 becoming 35
  - empty parentheses (an opening parenthesis immediately followed by a 
  closing one), which `eval()` would otherwise evaluate to an empty tuple 
  instead of a number
  - negative hand indices
  - repeated hand indices

Other malformed placements, such as a trailing operator or a card next 
to a parenthesis, are left to `eval()`, which rejects them. A mis-click 
is not prevented by any live validation (SPEC §5), so this check is what 
catches it.

```python
def is_valid_token_chain(tokens: list[int | str]) -> bool:
    """Check whether a token chain is well-formed enough to evaluate.

    Parameters
    ----------
    tokens : list[int | str]
        The clicked tokens, in order. Each token is an int (an index
        into the hand) or a str (one of "+", "-", "*", "/", "(", ")").

    Returns
    -------
    bool
        False if:
        - tokens is empty
        - an operator token ("+", "-", "*", "/") is not immediately 
        preceded by an int or a ")"
        - two int tokens are adjacent
        - a "(" is immediately followed by a ")" (empty parentheses, 
        which eval() would evaluate to an empty tuple)
        - a leading or post-"(" operator
        - two operators in a row, which would otherwise be silently 
        accepted by Python's eval() as unary plus/minus or as the 
        exponent and floor-division operators
        - adjacent ints
        - negative hand indices
        - repeated hand indices
        True otherwise. This does not guarantee the chain is fully valid 
        (e.g. unbalanced parentheses are not checked here); it only 
        catches cases eval() would not raise on by itself. Any other 
        malformed case is still caught by evaluate()'s own try/except 
        around eval().

    Raises
    ------
    IndexError
        If an int token is negative. This is a bug in the caller, not a 
        player error, so it is deliberately not caught by the try/except 
        in 'evaluate()'.
    """
    if not tokens:
        return False

    operators = ("+", "-", "*", "/")

    hand_idxs = []
    for index, token in enumerate(tokens):

        previous = tokens[index - 1] if index > 0 else None
        
        if token in operators:
            if previous is None:
                return False
            if not isinstance(previous, int) and previous != ")":
                return False

        if isinstance(token, int):
            hand_idxs.append(token)
            if token < 0:
                raise IndexError(f"Negative card index value")
            if isinstance(previous, int):
                return False

        if token == ")" and previous == "(":
            return False

    if len(hand_idxs) != len(set(hand_idxs)):
        raise ValueError(f"Repeated index in token chain")
        
    return True
```

### evaluate.py
`evaluate.py` holds a single function, `evaluate(tokens: list[int | str],
hand: list[int], target: int)`, and it is the one place in the codebase
that turns a completed token chain into a correct/wrong/error result
— it owns the entire win-check, not just the arithmetic. It takes the
token chain straight from `KryptoApp`, with no conversion beforehand.
It calls `is_valid_token_chain()` from `is_valid_token_chain.py` first;
if that returns `False`, it returns `(False, False, None)` immediately.
Otherwise it calls `build_expr_string()` from `build_expr_string.py` to
turn the tokens into a string. Every number in that string is rewritten
as `Fraction(<value>)`, so all the arithmetic is exact rational math
instead of floating point: `1/3*3` is exactly 1, a correct answer is
never rejected because of rounding error, and a division by zero raises
a catchable `ZeroDivisionError` instead of producing `inf` or `nan`.
Then it evaluates that string.
```python
import re
from fractions import Fraction

from krypto.build_expr_string import build_expr_string
from krypto.is_valid_token_chain import is_valid_token_chain


def evaluate(
    tokens: list[int | str], hand: list[int], target: int
) -> tuple[bool, bool, Fraction | None]:
    """Evaluate a token chain and check it against the target.

    `tokens` is the token chain exactly as KryptoApp built it from the
    player's clicks: each token is an int (an index into `hand`) or a
    str (one of "+", "-", "*", "/", "(", ")"). evaluate() first checks
    the chain with is_valid_token_chain() and, if that fails, returns
    right away as an invalid expression. Otherwise, it calls
    build_expr_string() to turn the tokens into a plain string (e.g.
    "3+5*2" or "(3+5)*2"), rewrites every number in that string as
    Fraction(<value>), and calls Python's eval() with an empty
    __builtins__ dict. The whole computation therefore happens over
    exact rationals rather than floats, and a genuine divide-by-zero
    raises a catchable ZeroDivisionError instead of producing inf or
    nan. Any exception raised during the rewrite or the eval() call —
    SyntaxError, ZeroDivisionError, TypeError, or anything else — is
    caught and treated as an invalid expression, never allowed to
    propagate to the caller. gui.py is not permitted to contain
    evaluation logic, so it never builds or wraps the string itself.

    Parameters
    ----------
    tokens : list[int | str]
        The clicked tokens, in order, as built by KryptoApp.
    hand : list[int]
        The round's five hand cards, in dealt order. An int token is an
        index into this list.
    target : int
        The round's target number to check the result against.

    Returns
    -------
    tuple[bool, bool, Fraction | None]
        A three-item tuple: ``(is_valid, is_win, value)``.

        - ``is_valid`` is False only when the expression could not be
          computed at all (a token chain rejected by
          is_valid_token_chain(), unbalanced parens, trailing operator,
          division by zero, etc.), in which case ``value`` is None and
          ``is_win`` is always False.
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
    IndexError
        If an int token is positive and outside the range of `hand`. 
        This is a bug in the caller, not a player error, so it is 
        deliberately not caught. Exceptions raised while evaluating the 
        expression (SyntaxError, ZeroDivisionError, TypeError) are caught 
        and reported through the return value.

    Notes
    -----
    evaluate() does not compute cards_used/score. That is derived by
    the caller, by counting the int tokens in the token list.
    """
    if not is_valid_token_chain(tokens):
        return False, False, None

    expr_str = build_expr_string(tokens, hand)
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
`average_score`, and `average_time_5_card`. `score_counts` is a dict 
that holds the 0–5 breakdown, where a give-up counts as score 0 and a 
win's score is its `cards_used`. `total_games` is the record count. 
`average_score` is the mean of `cards_used` across every record, with 
give-ups included as 0. `average_time_5_card` is the mean `time_sec` 
across only the wins where `cards_used == 5`. If there are no records, 
`score_counts` still has all six keys (0 through 5) with a count of 0, 
`total_games` is 0, and both averages are `None`. `average_time_5_card` 
is also `None` whenever there are no 5-card wins, even if other records 
exist. Neither average is ever computed by dividing by zero.

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
`how_to_play`, and `exit`. `gui.py` just applies each value from this 
dict to the matching button, it doesn't compute any of them itself.
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
It's called once, from `main.py`, and blocks until the window is closed. 
`KryptoApp` registers its Exit handler for the `WM_DELETE_WINDOW` 
protocol, so the OS window-close button behaves exactly like the "Exit" 
button. 

`KryptoApp`:
- owns the round state (`"not_started"`/`"in_progress"`/`"won"`/`"given_up"`)
- owns the current `target`/`hand`
- owns the ordered token list
- creates every widget from the "Game Layout" diagram below 
- formats the timer display and result messages itself (§7.3)

Everything else is delegated to other functions. 

`KryptoApp` starts in `"not_started"` on launch (SPEC §7.2) and no deal 
happens until "Start New Game" is clicked.

When "Start New Game" is clicked, it:
- calls `deal()` from `deal.py` to get a fresh `(target, hand)`
- clears the token list
- sets the round state to `"in_progress"`
- records `start_time = time.monotonic()`
- begins a recurring `.after()` call that updates the displayed timer 
while in progress.

Its token list holds items that are either an `int` (the index of a 
clicked hand card into `hand`) or a `str` (one of `+ - * / ( )`, a 
clicked symbol) — see `build_expr_string.py`. On each state or token 
change it calls `get_available_controls()` and applies the result to 
the buttons. Clicking a hand card appends its index to the token list 
and disables the card in the gui. If "Undo" pops an `int` token, then 
that hand card button is re-enabled.

- "Clear" (only available while in progress and the token list is 
non-empty) empties the token list. Every hand card button is re-enabled, 
because `get_available_controls()` is recomputed from the now-empty 
list.

- "Submit" calls `evaluate(tokens, hand, target)` with the current token 
list; `KryptoApp` never builds or validates the expression string from 
the token list itself. Submit then uses the returned `(is_valid, is_win, 
value)` tuple:
  - If `is_valid` is `False`, it shows an error message, the round stays 
  in progress, and the expression and timer are left untouched.
  - If `is_valid` is `True` but `is_win` is `False`, it shows the returned 
  `value` as the result of the player's expression, the round stays in 
  progress, and the expression and timer are left untouched. 
  - If `is_win` is `True`:
    - it computes `time_sec = time.monotonic() - start_time`
    - calls `append_result()`
    - sets the round state to `"won"`
    - cancels the recurring `.after()` timer update, so the displayed 
    time stays frozen at its final value 
    - refreshes the buttons through `get_available_controls()`, which is 
    what makes "Start New Game" available again
    - leaves the expression, target, and final time on screen until 
    "Start New Game" is clicked.

- "Give Up" (only available while in-progress) asks for confirmation.
  - If a confirmed Give Up:
    - it computes `time_sec = time.monotonic() - start_time` 
    - calls `append_result()`
    - sets the round state to `"given_up"`
    - cancels the recurring `.after()` timer update, so the displayed 
    time stays frozen at its final value 
    - refreshes the buttons through `get_available_controls()`, which is 
    what makes "Start New Game" available again
    - leaves the expression, target, and final time on screen until 
    "Start New Game" is clicked. 

- "Exit" checks the round state first.
  - If the state is `"in_progress"`, it asks for confirmation. 
    - If a confirmed Exit:
      - it computes `time_sec = time.monotonic() - start_time` 
      - calls `append_result()` the same way "Give Up" does
      - closes the window.
      - A confirmed Exit needs no state change, because the window closes 
      immediately.
  - If the state is `"not_started"`, `"won"`, or `"given_up"`, it closes 
  the window immediately, with no confirmation and no call to 
  `append_result()`.

- "Stats" opens a `StatsWindow`.  See `stats_window.py`.

- "How to Play" opens a small read-only window, built and handled 
entirely inside `KryptoApp` by a private method, with no separate file 
or class for it. The window is a `tk.Toplevel` that holds the rules text 
in a `tk.Label` and a Close button. The text must be copied word for word 
from the SPEC §7.7 mockup, not paraphrased. The window is modal (made 
with `transient()` and `grab_set()`), so the main window cannot be used 
while it is open. The `how_to_play` button is only available when no 
round is in progress, so the timer is never running while it is open.

Game layout (SPEC §7.1):
```
+----------------------------------------------------------+
|  Krypto                            [How to Play] [Stats] |
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
the only place the "Stats" screen (§7.5) is built and shown. It owns 
only its own window and Close button; it never touches `KryptoApp`'s 
state. It is modal (made with `transient()` and `grab_set()`), and the 
`Stats` button is only available when no round is in progress, so the 
timer is never running while it is open. It's opened by `gui.py`'s 
"Stats" button and takes no game state from `KryptoApp` at construction 
time — instead it builds the "Stats" screen from the history file, if 
it exists. This is done by calling `load_history()`, `derive_stats()`, 
and `derive_best_times()` to get fresh numbers every time it opens, per 
§7.4. Each best-time record's `hand` comes in as `list[int]` (from 
`load_history()`, via `derive_best_times()`); `stats_window.py` joins 
it into a comma-separated string (e.g. `"1,3,6,12,21"`) for the table — 
this formatting is the only place it happens, and it stays `list[int]` 
everywhere upstream. When `average_score` or `average_time_5_card` from 
`derive_stats()` is `None`, the table shows "N/A" in its place instead 
of a number. When `derive_best_times()` returns an empty list, the Top 
10 section simply shows no rows.

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
— it starts with no round in progress, and clicking "Start New Game" is
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

### test_is_valid_token_chain.py
```python
import pytest

from krypto.is_valid_token_chain import is_valid_token_chain


def test_empty_token_chain_is_invalid():
    assert is_valid_token_chain([]) is False


@pytest.mark.parametrize(
    "tokens",
    [
        [0, "+", "+", 1],
        [0, "-", "-", 1],
        [0, "*", "*", 1],
        [0, "/", "/", 1],
        [0, "+", "-", 1],
        [0, "-", "*", 1],
        ["(", "(", 0, "+", "+", 1, ")", ")"],
    ],
)
def test_two_operators_in_a_row_is_invalid(tokens):
    assert is_valid_token_chain(tokens) is False


@pytest.mark.parametrize(
    "tokens",
    [
        [0, 1],
        [0, 1, 2],
        [0, "+", 1, 2],
        ["(", 0, 1, ")"],
    ],
)
def test_two_cards_in_a_row_is_invalid(tokens):
    # Adjacent cards would be joined into one multi-digit number.
    assert is_valid_token_chain(tokens) is False


@pytest.mark.parametrize(
    "tokens",
    [
        ["-", 0, "+", 1],
        ["+", 0],
        ["*", 0],
        ["/", 0],
    ],
)
def test_leading_operator_is_invalid(tokens):
    assert is_valid_token_chain(tokens) is False


@pytest.mark.parametrize(
    "tokens",
    [
        ["(", "-", 0, "+", 1, ")"],
        ["(", "+", 0, ")"],
        [0, "*", "(", "-", 1, ")"],
    ],
)
def test_operator_right_after_open_paren_is_invalid(tokens):
    assert is_valid_token_chain(tokens) is False


@pytest.mark.parametrize(
    "tokens",
    [
        ["(", ")"],
        ["(", "(", ")", ")"],
        [0, "+", "(", ")"],
    ],
)
def test_empty_parentheses_is_invalid(tokens):
    assert is_valid_token_chain(tokens) is False


@pytest.mark.parametrize(
    "tokens",
    [
        [0, "+", 0],
        [0, "+", 1, "*", 0],
        ["(", 0, "+", 1, ")", "*", 0],
    ],
)
def test_repeated_card_index_raises_value_error(tokens):
    # Each card can be used once. The UI prevents a repeat, so one arriving
    # here is a bug in the caller and is deliberately not caught.
    with pytest.raises(ValueError):
        is_valid_token_chain(tokens)


@pytest.mark.parametrize(
    "tokens",
    [
        [-1],
        [0, "+", -1],
    ],
)
def test_negative_card_index_raises_index_error(tokens):
    # hand[-1] would silently return the last card, so a negative index
    # must fail loudly instead.
    with pytest.raises(IndexError):
        is_valid_token_chain(tokens)


@pytest.mark.parametrize(
    "tokens",
    [
        [0, "+", 1],
        [0, "-", 1],
        [0, "*", 1],
        [0, "/", 1],
        [2],
        ["(", 0, "+", 1, ")", "*", 2],
        ["(", 0, "+", 1, ")", "-", 2],
        ["(", "(", "(", 0, "+", 1, ")", "*", 2, ")", "-", 3, ")", "+", 4],
    ],
)
def test_well_formed_chains_are_valid(tokens):
    assert is_valid_token_chain(tokens) is True


@pytest.mark.parametrize(
    "tokens",
    [
        [0, "+"],
        ["(", 0, "+", 1],
        [0, "(", 1, ")"],
    ],
)
def test_other_malformed_chains_are_left_to_eval(tokens):
    # A trailing operator, unbalanced parentheses, and a card next to a
    # parenthesis are not this function's job; evaluate() rejects them.
    assert is_valid_token_chain(tokens) is True
```

### test_evaluate.py
```python
import pytest
from fractions import Fraction

from krypto.evaluate import evaluate

HAND = [3, 5, 2, 12, 21]


def test_empty_token_chain_is_invalid():
    assert evaluate([], HAND, 5) == (False, False, None)


def test_adjacent_operators_is_invalid():
    assert evaluate([0, "+", "+", 1], HAND, 8) == (False, False, None)


def test_two_cards_in_a_row_is_invalid():
    # Cards 3 and 5 must not be joined into the number 35.
    assert evaluate([0, 1], HAND, 35) == (False, False, None)


def test_leading_operator_is_invalid():
    assert evaluate(["-", 0, "+", 1], HAND, 2) == (False, False, None)


def test_operator_after_open_paren_is_invalid():
    tokens = ["(", "-", 0, "+", 1, ")"]
    assert evaluate(tokens, HAND, 2) == (False, False, None)


def test_unbalanced_parens_is_invalid():
    is_valid, is_win, value = evaluate(["(", 0, "+", 1], HAND, 8)
    assert is_valid is False
    assert is_win is False
    assert value is None


def test_trailing_operator_is_invalid():
    assert evaluate([0, "+"], HAND, 3) == (False, False, None)


def test_empty_parentheses_is_invalid():
    # eval("()") would otherwise return an empty tuple, not a number.
    assert evaluate(["(", ")"], HAND, 5) == (False, False, None)


def test_division_by_zero_is_invalid():
    hand = [3, 4, 4, 8, 12]
    tokens = [0, "/", "(", 1, "-", 2, ")"]
    assert evaluate(tokens, hand, 1) == (False, False, None)


def test_valid_expression_wrong_answer():
    is_valid, is_win, value = evaluate([0, "+", 1], HAND, 9)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(8)


def test_valid_expression_correct_answer_is_win():
    is_valid, is_win, value = evaluate([0, "+", 1], HAND, 8)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(8)


def test_parens_and_precedence():
    tokens = ["(", 0, "+", 1, ")", "*", 2]
    is_valid, is_win, value = evaluate(tokens, HAND, 16)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(16)


def test_exact_fraction_arithmetic_no_float_error():
    # 1/3 * 3 must equal exactly 1 with Fraction, unlike float math.
    hand = [1, 3, 3, 8, 12]
    is_valid, is_win, value = evaluate([0, "/", 1, "*", 2], hand, 1)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(1)


def test_fractional_result_not_matching_target():
    hand = [1, 3, 5, 8, 12]
    is_valid, is_win, value = evaluate([0, "/", 1], hand, 1)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(1, 3)


def test_negative_intermediate_result_not_matching_target():
    is_valid, is_win, value = evaluate([0, "-", 1], HAND, 2)
    assert is_valid is True
    assert is_win is False
    assert value == Fraction(-2)


def test_single_card_can_win():
    is_valid, is_win, value = evaluate([1], HAND, 5)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(5)


def test_max_depth_parens():
    hand = [1, 2, 3, 4, 5]
    tokens = ["(", "(", "(", 0, "+", 1, ")", "*", 2, ")", "-", 3, ")", "+", 4]
    is_valid, is_win, value = evaluate(tokens, hand, 10)
    assert is_valid is True
    assert is_win is True
    assert value == Fraction(10)


def test_index_outside_hand_raises_index_error():
    # A bad index is a bug in the caller, so it is deliberately not caught.
    with pytest.raises(IndexError):
        evaluate([9], HAND, 1)
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
Runs `deal()` with a seeded random source, calls `evaluate()` with a 
fixed token list that is known to calculate to the target, then asserts 
the result is correct. `evaluate()` calls `is_valid_token_chain()` and 
`build_expr_string()` internally, so this exercises all four modules 
together.
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
