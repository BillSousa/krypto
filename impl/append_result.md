## Product Specification
### 6. Persistence — History & Stats

- Persistence is a single flat, human-readable history file located in 
  the same folder next to the program itself.
- One entry is recorded in the history file per **concluded** round only:
  - a win, 
  - a confirmed "Give Up", or 
  - a confirmed "Exit" while a round is in progress.
- A failed "Submit" attempt (incorrect result or invalid expression) 
  records nothing, and neither does "Exit" when no round is in progress.
- Each entry captures: timestamp, target, the hand dealt, result
  (win/give-up), number of cards used, and time taken.
- A single unreadable or corrupted entry must not prevent the rest of
  the history from being read, and must not crash the stats view.
- No pruning or size limit is needed — at realistic play volumes the
  history file stays small (well under a few MB even after tens of
  thousands of rounds).

## Implementation
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
