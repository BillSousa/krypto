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
