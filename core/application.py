"""
Application bootstrap.
"""

from __future__ import annotations

from ui.main_window import MainWindow


class Application:
    """Main application controller."""

    def __init__(self) -> None:
        self.main_window = MainWindow()

    def start(self) -> None:
        """Start application."""
        self.main_window.show()