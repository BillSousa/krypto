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
