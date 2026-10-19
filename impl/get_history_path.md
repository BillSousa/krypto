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
