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

