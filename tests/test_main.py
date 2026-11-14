import runpy
from typing import Any

import pytest

import krypto.gui
import krypto.main
from krypto.main import main


class FakeKryptoApp:
    """Stand-in for KryptoApp that records construction and mainloop calls."""

    instances: list["FakeKryptoApp"] = []

    def __init__(self) -> None:
        """Record that an instance was created.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.mainloop_calls: int = 0
        FakeKryptoApp.instances.append(self)

    def mainloop(self, n: int = 0) -> None:
        """Record a call to mainloop.

        Parameters
        ----------
        n : int
            Accepted for signature compatibility with tk.Tk.mainloop.

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.mainloop_calls += 1


@pytest.fixture
def fake_app(monkeypatch: pytest.MonkeyPatch) -> type[FakeKryptoApp]:
    """Replace KryptoApp with FakeKryptoApp for the duration of a test.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        Pytest monkeypatch fixture.

    Returns
    -------
    type[FakeKryptoApp]
        The fake class, with its instance list reset.

    Raises
    ------
    None
    """
    FakeKryptoApp.instances = []
    monkeypatch.setattr(krypto.main, "KryptoApp", FakeKryptoApp)
    return FakeKryptoApp


def test_main_creates_one_app(fake_app: type[FakeKryptoApp]) -> None:
    """main() constructs exactly one KryptoApp.

    Parameters
    ----------
    fake_app : type[FakeKryptoApp]
        Fake KryptoApp class.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    main()
    assert len(fake_app.instances) == 1


def test_main_runs_mainloop_once(fake_app: type[FakeKryptoApp]) -> None:
    """main() runs the Tkinter event loop exactly once.

    Parameters
    ----------
    fake_app : type[FakeKryptoApp]
        Fake KryptoApp class.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    main()
    assert fake_app.instances[0].mainloop_calls == 1


def test_main_returns_none(fake_app: type[FakeKryptoApp]) -> None:
    """main() returns None.

    Parameters
    ----------
    fake_app : type[FakeKryptoApp]
        Fake KryptoApp class.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    result: Any = main()
    assert result is None


def test_running_as_script_invokes_main(
    fake_app: type[FakeKryptoApp], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Running krypto.main as __main__ builds the app and runs mainloop.

    Parameters
    ----------
    fake_app : type[FakeKryptoApp]
        Fake KryptoApp class.
    monkeypatch : pytest.MonkeyPatch
        Pytest monkeypatch fixture.

    Returns
    -------
    None

    Raises
    ------
    None
    """
    monkeypatch.setattr(krypto.gui, "KryptoApp", FakeKryptoApp)
    runpy.run_path(krypto.main.__file__, run_name="__main__")
    assert len(fake_app.instances) == 1
    assert fake_app.instances[0].mainloop_calls == 1
