from __future__ import annotations

import math
import re

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
)


class CommandLine(QWidget):
    """
    Command Line for MCI SoftEngine.

    Supported command examples:

        LINE 0,0 500,0
        RECTANG 0,0 700,400
        CIRCLE 300,200 100
        PLINE 0,0 500,0 500,300 0,300 CLOSE

    Coordinate formats:

        100,200          absolute
        @100,200         relative
        @100<45          polar
    """

    commandEntered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel("Command:")

        self.edit = QLineEdit()
        self.edit.setPlaceholderText(
            "LINE 0,0 500,0"
        )

        self.edit.returnPressed.connect(
            self._send_command
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)

        layout.addWidget(self.label)
        layout.addWidget(self.edit)

        self.setLayout(layout)

    # ---------------------------------------------------------
    # Send command
    # ---------------------------------------------------------

    def _send_command(self):
        text = self.edit.text().strip()

        if not text:
            return

        self.commandEntered.emit(text)

        self.edit.clear()

    # ---------------------------------------------------------
    # Prompt
    # ---------------------------------------------------------

    def set_prompt(self, text: str):
        self.label.setText(str(text))

    # ---------------------------------------------------------
    # Text
    # ---------------------------------------------------------

    def set_text(self, text: str):
        self.edit.setText(str(text))

        self.edit.setFocus()

        self.edit.setCursorPosition(
            len(self.edit.text())
        )

    def text(self) -> str:
        return self.edit.text()

    def clear(self):
        self.edit.clear()

    def focus(self):
        self.edit.setFocus()

    # ---------------------------------------------------------
    # Command parser helpers
    # ---------------------------------------------------------

    @staticmethod
    def tokenize(command: str) -> list[str]:
        """
        Split command into tokens while preserving
        coordinate expressions such as:

            100,200
            @100,200
            @100<45
        """

        return command.strip().split()

    @staticmethod
    def command_name(command: str) -> str:
        """
        Return command name in uppercase.

        Example:
            'line 0,0 100,100'
            -> 'LINE'
        """

        tokens = CommandLine.tokenize(command)

        if not tokens:
            return ""

        return tokens[0].upper()

    @staticmethod
    def parse_number(value: str) -> float:
        """
        Convert text to a floating-point number.
        """

        return float(value.strip())

    @staticmethod
    def parse_point(value: str) -> tuple[float, float]:
        """
        Parse absolute coordinates.

        Examples:

            100,200
            0,0
            -50.5,200.25
        """

        value = value.strip()

        if value.startswith("@"):
            value = value[1:]

        if "<" in value:
            raise ValueError(
                "Polar coordinate requires a base point."
            )

        if "," not in value:
            raise ValueError(
                f"Invalid point: {value}"
            )

        x_text, y_text = value.split(",", 1)

        return (
            float(x_text),
            float(y_text),
        )

    @staticmethod
    def parse_relative_point(
        value: str,
        base_x: float,
        base_y: float,
    ) -> tuple[float, float]:
        """
        Parse absolute, relative or polar point.

        Examples:

            100,200

            @100,50

            @100<45
        """

        value = value.strip()

        # Absolute
        if not value.startswith("@"):
            return CommandLine.parse_point(value)

        value = value[1:]

        # Polar coordinate
        if "<" in value:
            distance_text, angle_text = value.split(
                "<",
                1,
            )

            distance = float(distance_text)
            angle = math.radians(
                float(angle_text)
            )

            x = base_x + distance * math.cos(angle)
            y = base_y + distance * math.sin(angle)

            return x, y

        # Relative Cartesian
        if "," not in value:
            raise ValueError(
                f"Invalid relative point: @{value}"
            )

        dx_text, dy_text = value.split(",", 1)

        dx = float(dx_text)
        dy = float(dy_text)

        return (
            base_x + dx,
            base_y + dy,
        )

    @staticmethod
    def parse_distance(value: str) -> float:
        """
        Parse a distance.

        Example:

            100
            250.5
        """

        value = value.strip()

        return float(value)

    # ---------------------------------------------------------
    # Command validation
    # ---------------------------------------------------------

    @staticmethod
    def is_supported_command(command: str) -> bool:
        """
        Check whether a command is recognized.
        """

        supported = {
            "LINE",
            "PLINE",
            "RECTANG",
            "CIRCLE",
            "ARC",
            "POINT",
            "POLYGON",
            "ELLIPSE",

            "MOVE",
            "COPY",
            "ROTATE",
            "SCALE",
            "MIRROR",
            "OFFSET",
            "TRIM",
            "EXTEND",
            "FILLET",
            "CHAMFER",
            "STRETCH",
            "ARRAY",
            "ERASE",

            "DIM",
            "DIMLINEAR",
            "DIMALIGNED",
            "DIMANGULAR",
            "DIMRADIUS",
            "DIMDIAMETER",

            "ZOOM",
            "PAN",
            "REDRAW",
            "REGEN",

            "UNDO",
            "REDO",
        }

        return (
            CommandLine.command_name(command)
            in supported
        )