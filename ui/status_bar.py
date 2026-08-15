from PySide6.QtWidgets import QStatusBar, QLabel
from PySide6.QtCore import Qt


class StatusBar(QStatusBar):
    """Status bar for MCI SoftEngine."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # ارتفاع نوار وضعیت
        self.setFixedHeight(32)

        # =================================================
        # مختصات
        # =================================================

        self.coordinates_label = QLabel(
            "X: 0.00    Y: 0.00"
        )

        self.coordinates_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.coordinates_label.setMinimumWidth(260)

        self.coordinates_label.setStyleSheet(
            """
            QLabel {
                color: white;
                background-color: #202020;
                border: 1px solid #555555;
                padding: 4px 12px;
                font-size: 13px;
                font-weight: bold;
            }
            """
        )

        # قرار دادن مختصات در سمت راست StatusBar
        self.addPermanentWidget(
            self.coordinates_label
        )

        # =================================================
        # ظاهر StatusBar
        # =================================================

        self.setStyleSheet(
            """
            QStatusBar {
                background-color: #303030;
                color: white;
                border-top: 1px solid #555555;
            }

            QStatusBar::item {
                border: none;
            }
            """
        )

    # =====================================================
    # مختصات
    # =====================================================

    def set_coordinates(self, x, y):

        self.coordinates_label.setText(
            f"X: {x:.2f}    Y: {y:.2f}"
        )

    # =====================================================
    # نمایش مختصات
    # =====================================================

    def show_coordinates(self, x, y):

        self.set_coordinates(x, y)

    # =====================================================
    # Reset
    # =====================================================

    def reset_coordinates(self):

        self.set_coordinates(
            0.0,
            0.0
        )

    # =====================================================
    # پیام
    # =====================================================

    def set_message(self, message):

        self.showMessage(
            str(message)
        )