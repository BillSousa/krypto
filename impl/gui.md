## Product Specification
### 5. Input Model

- All input is click-driven: the player clicks card, operator (`+ - *
  /`), and parenthesis buttons to build an expression left to right. No
  free typing at any point.
- The expression area itself is display-only and is never clicked, either 
  to add or to remove tokens.
- Each hand card can be placed at most once; placing it disables that
  card's button until it's removed from the expression.
- Two ways to remove tokens from the expression:
  - an Undo button that removes the most-recently-placed token, one at a 
  time, or 
  - a Clear button that wipes the whole expression.
- Up to 3 opening and 3 closing parentheses may be placed (§4).
- The expression area has a fixed maximum length of 15 symbols (5
  numbers + 4 operators + 6 parentheses — the worst case allowed by the
  rules above), rather than growing or scrolling. Once 15 symbols are
  placed, no more symbols can be added until Undo or Clear frees space.
- Submit is always available while a round is in progress, whatever the
  expression looks like; there is no live well-formedness checking as 
  the expression is built. An incomplete or invalid expression simply 
  fails on Submit with an error message — the player can keep adjusting.

### 7.1 Game Layout

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

- The window has a fixed size and does not resize, keeping the layout
  predictable.
- The "Stats" and "How to Play" buttons are always visible, but available
  only when no round is in progress (not started, won, or given up), so
  the timer is never running while either window is open. "Stats" opens 
  a separate view (§7.4); "How to Play" opens a separate text window 
  (§7.6, §7.7). Each window is modal: the main window cannot be used 
  until the window is closed with its Close button. There is no 
  pause/resume mechanism.

### 7.3 Submit / Give Up / Exit Behavior

- **Submit:**
  - On success — stop the timer, record a win (§6), show a success 
  message (e.g. "Solved with 4 cards in 42.7s!"). 
  - On failure for wrong result — stay in progress, show an error message 
  that displays the result of their expression to the user, leave the 
  expression and timer untouched so the player can keep adjusting.
  - On failure for invalid expression — stay in progress, show an error
  message, leave the expression and timer untouched so the player can
  keep adjusting.
  
- **Give Up:** asks for Yes/No confirmation. "No" changes nothing. "Yes"
  — stop the timer, record a give-up with a score of 0 (§6), show a
  neutral message but never a correct solution (§2).

- **Exit:**
  - When a round is in progress, it asks for Yes/No confirmation, same 
  as "Give Up". "No" changes nothing. "Yes" — stop the timer, record a 
  give-up with a score of 0 (§6), then close the GUI entirely.
  - When no round is in progress (not started, won, or given up), it 
  just closes the window, with no give-up recorded.
  - The window's own close button (the X in the title bar) behaves 
  exactly like the Exit button in every case above.

### 7.4 "Stats" Behavior
See stats_window.md

### 7.6 "How to Play" Text Box Behavior

Opened via the "How to Play" button, in the top bar next to "Stats", 
which is available only when no round is in progress. It appears as a
separate, modal, read-only window containing the rules text and a Close
button. Like the "Stats" window, it can only be open while no round is
running, so it never affects the timer. The text covers the rules of this
version of Krypto, not necessarily how to use the buttons; the layout is 
expected to be largely self-explanatory.

### 7.7 "How to Play" Text Box Display

```
+----------------------------------------------------------+
|                       How to Play                        |
+----------------------------------------------------------+
|  - Each round deals a target number and five hand cards  |
|    (1 to 25) from a 56-card deck.                        |
|  - Combine the hand cards with the aritmetic operators   |
|    (+ - * /) and parentheses to make an expression that  |
|    equals the target exactly.                            |
|  - Each hand card can only be used once. You do not have |
|    to use all five cards. Your score is the number of    |
|    cards you used, from 1 to 5.                          |
|  - Negative and fractional values are allowed in the     |
|    middle of a calculation. Only the final result has    |
|    to equal the target.                                  |
|  - Give Up and Exit end the round with a score of 0.     |
|  - The timer counts up from the moment you click Start   |
|    New Game, and stops when you solve the round or give  |
|    up.                                                   |
+----------------------------------------------------------+
|                        [ Close ]                         |
+----------------------------------------------------------+
```

### 10. Open Questions

- GUI visual polish (colors, fonts, exact sizing) — left to iterate
  against a working prototype.

## Implementation
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