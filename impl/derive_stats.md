## Product Specification
N/A

## Implementation
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