from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from renderer.renderer import Renderer


def main():

    app = QApplication(sys.argv)

    window = MainWindow()

    renderer = Renderer()

    window.set_renderer(
        renderer
    )

    window.set_entities(
        []
    )

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()