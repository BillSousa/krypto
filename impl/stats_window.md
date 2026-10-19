## Product Specification
### 7.4 "Stats" Behavior

Opened via the "Stats" button, which is available only when no round is 
in progress. Recomputed fresh from the history (§6) every time it's 
opened, not cached separately, so there's no separate state that can 
drift out of sync. 
Shows:
  - a give-up / exit count,
  - a breakdown of wins by cards used (1–5) with count, 
  - games played = total rounds recorded, 
  - average score,
  - average time (for 5-card wins only),
  - best times (for the top 10 5-card wins only). 

### 7.5 "Stats" GUI
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

## Implementation
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