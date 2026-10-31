from pathlib import Path
import sys

def get_history_path() -> Path:
    """
    Returns the path to the history file located in the same directory as the krypto game executable.
    When frozen by PyInstaller, that's Path(sys.executable).parent; when run as a plain script that's,
    Path(__file__).resolve().parent.
    """
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent / 'krypto_history.txt'
    else:
        return Path(__file__).resolve().parent / 'krypto_history.txt'
