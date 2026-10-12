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
