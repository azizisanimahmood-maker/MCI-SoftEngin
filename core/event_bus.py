from __future__ import annotations

from collections import defaultdict
from typing import Callable


class EventBus:
    """Simple application-wide event bus."""

    def __init__(self):
        self._listeners = defaultdict(list)

    # =====================================================
    # SUBSCRIBE
    # =====================================================

    def subscribe(self, event_name: str, callback: Callable):
        if not callable(callback):
            raise TypeError("callback must be callable")

        if callback not in self._listeners[event_name]:
            self._listeners[event_name].append(callback)

        return callback

    # =====================================================
    # UNSUBSCRIBE
    # =====================================================

    def unsubscribe(self, event_name: str, callback: Callable):
        listeners = self._listeners.get(event_name, [])

        if callback in listeners:
            listeners.remove(callback)
            return True

        return False

    # =====================================================
    # EMIT
    # =====================================================

    def emit(self, event_name: str, *args, **kwargs):
        listeners = list(
            self._listeners.get(event_name, [])
        )

        for callback in listeners:
            callback(*args, **kwargs)

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self, event_name: str | None = None):
        if event_name is None:
            self._listeners.clear()
        else:
            self._listeners.pop(event_name, None)

    # =====================================================
    # LISTENERS
    # =====================================================

    def listener_count(self, event_name: str) -> int:
        return len(
            self._listeners.get(event_name, [])
        )
