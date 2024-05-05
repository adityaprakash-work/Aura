# ---INFO-----------------------------------------------------------------------
"""
PyDiv widget for the application.
"""


# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtWidgets as qtw


# ---SRC------------------------------------------------------------------------
class PyDiv(qtw.QWidget):
    def __init__(self, color):
        super().__init__()

        self.layout = qtw.QHBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.frame_line = qtw.QFrame()
        self.frame_line.setStyleSheet(f"background: {color};")
        self.frame_line.setMaximumHeight(1)
        self.frame_line.setMinimumHeight(1)
        self.layout.addWidget(self.frame_line)
        self.setMaximumHeight(1)
