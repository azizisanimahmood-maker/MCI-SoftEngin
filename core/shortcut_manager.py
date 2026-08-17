from __future__ import annotations


class ShortcutManager:
    """Basic keyboard shortcut registry."""

    def __init__(self):
        self._shortcuts = {}

    # =====================================================
    # REGISTER
    # =====================================================

    def register(self, shortcut: str, command):
        if not shortcut:
            raise ValueError("shortcut cannot be empty")

        self._shortcuts[
            shortcut.upper()
        ] = command

    # =====================================================
    # UNREGISTER
    # =====================================================

    def unregister(self, shortcut: str):
        return self._shortcuts.pop(
            shortcut.upper(),
            None
        )

    # =====================================================
    # GET
    # =====================================================

    def get(self, shortcut: str, default=None):
        return self._shortcuts.get(
            shortcut.upper(),
            default
        )

    # =====================================================
    # EXISTS
    # =====================================================

    def contains(self, shortcut: str) -> bool:
        return shortcut.upper() in self._shortcuts

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):
        self._shortcuts.clear()

    # =====================================================
    # COUNT
    # =====================================================

    def count(self) -> int:
        return len(self._shortcuts)

    # =====================================================
    # ALL
    # =====================================================

    def all(self):
        return dict(self._shortcuts)
