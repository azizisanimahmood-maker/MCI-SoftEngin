from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from core.document import Document
from ui.main_window import MainWindow
from renderer.renderer import Renderer


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
    # RENDERER
    # =================================================

    renderer = Renderer()

    window.set_renderer(
        renderer
    )

    # =================================================
    # SHARED ENTITY STORAGE
    # =================================================
    # Canvas and Document use the SAME entity list.

    window.set_entities(
        document.entities
    )

    # Keep a reference to the document on the window.
    window.document = document

    # =================================================
    # SHOW
    # =================================================

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()
