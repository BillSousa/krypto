## Product Specification
N/A

## Implementation
`main.py` is the entry point — it has no function or class of its own,
just top-level script code guarded by `if __name__ == "__main__":`. It
imports `KryptoApp` from `gui.py`, instantiates it, and calls
`.mainloop()`. Per SPEC §7.2, the app does not deal a round on launch
— it starts with no round in progress, and clicking "Start New Game" is
what triggers the first deal and starts the timer, same as every round
after. `main.py` itself never calls `deal()`; `KryptoApp` handles that
in response to the button. It has no PyInstaller-specific handling of
its own — that's entirely inside `get_history_path.py`.
```python
   <<<code body>>>
```
