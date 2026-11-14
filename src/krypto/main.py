from krypto.gui import KryptoApp


def main() -> None:
    """Launch the Krypto GUI and run the Tkinter event loop.

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
    app = KryptoApp()
    app.mainloop()


if __name__ == "__main__":
    main()
