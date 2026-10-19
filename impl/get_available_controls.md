## Product Specification
### 7.2 Round Lifecycle & Button Availability

A round is either **not started**, **in progress**, **won**, or **given
up**. The app launches in the not started state — no deal happens until
the user clicks "Start New Game", which loads a fresh deal and starts
the timer.

| Control | Available when |
|---|---|
| Each hand-card button | In progress and not yet placed; re-enabled if removed from expression |
| `+ - * /` buttons | In progress and fewer than 15 symbols placed |
| `(` button | In progress, fewer than 15 symbols placed, fewer than 3 open parentheses placed so far |
| `)` button | In progress, fewer than 15 symbols placed, at least one currently-unclosed `(` exists |
| Undo | In progress and the expression is non-empty |
| Clear | In progress and the expression is non-empty |
| Submit | Only while in progress; even on an empty expression this fails gracefully, see §5 |
| Give Up | Only while in progress; asks for Yes/No confirmation |
| Start New Game | Only when no round is in progress (not started, won, or given up) — **never** mid-round |
| Stats | Only when no round is in progress (not started, won, or given up) |
| How to Play | Only when no round is in progress (not started, won, or given up) |
| Exit | Always. While a round is in progress: asks for Yes/No confirmation, records a give-up, and closes the GUI. Otherwise: closes the GUI immediately, with no give-up recorded |

- There is deliberately no way to leave a round unrecorded. Since "Start
  New Game" is unavailable during an active round, every round ends in
  exactly one of three ways: a correct "Submit", a confirmed "Give Up", 
  or a confirmed "Exit" (which records a give-up and closes the app).
- Once a round is won or given up, all input controls disable; the
  expression, target, and final time stay on screen exactly as they were
  at that moment, until "Start New Game" is clicked.
- The window's own close button (the X in the title bar) is not a row in
  the table above. It behaves exactly like "Exit" (§7.3).

## Implementation
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