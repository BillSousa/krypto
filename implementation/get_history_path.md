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
