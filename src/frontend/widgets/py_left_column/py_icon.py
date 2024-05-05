# ---INFO-----------------------------------------------------------------------
"""
PyIcon widget for the application.
"""


# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw


# ---SRC------------------------------------------------------------------------
class PyIcon(qtw.QWidget):
    def __init__(self, icon_path, icon_color):
        super().__init__()
        self._icon_path = icon_path
        self._icon_color = icon_color

        self.setup_ui()

    def setup_ui(self):
        self.layout = qtw.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.icon = qtw.QLabel()
        self.icon.setAlignment(qtc.Qt.AlignCenter)

        self.set_icon(self._icon_path, self._icon_color)
        self.layout.addWidget(self.icon)

    def set_icon(self, icon_path, icon_color=None):
        color = icon_color if icon_color else self._icon_color
        icon = qtg.QPixmap(icon_path)
        painter = qtg.QPainter(icon)
        painter.setCompositionMode(qtg.QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        painter.end()

        self.icon.setPixmap(icon)
