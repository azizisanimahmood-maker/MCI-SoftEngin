"""
MCI SoftEngine
Entry Point
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from core.application import Application


def main() -> int:
    qt_app = QApplication(sys.argv)
    qt_app.setApplicationName("MCI SoftEngine")
    qt_app.setOrganizationName("MCI")

    app = Application()
    app.start()

    return qt_app.exec()


if __name__ == "__main__":
    raise SystemExit(main())