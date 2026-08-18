from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from core.document import Document
from ui.main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    # =================================================
    # DOCUMENT
    # =================================================

    document = Document()

    # =================================================
    # MAIN WINDOW
    # =================================================

    window = MainWindow()

    # =================================================
    # SHARED DOCUMENT
    # =================================================

    window.document = document
    window.entities = document.entities

    window.canvas.set_entities(
        document.entities
    )

    # =================================================
    # SHOW
    # =================================================

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()