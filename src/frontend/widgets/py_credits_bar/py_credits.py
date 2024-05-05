# ---INFO-----------------------------------------------------------------------
"""
PyCredits widget for the application.
"""


# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw


# ---SRC------------------------------------------------------------------------
class PyCredits(qtw.QWidget):
    def __init__(
        self,
        copyright,
        version,
        bg_two,
        font_family,
        text_size,
        text_description_color,
        radius=8,
        padding=10,
    ):
        super().__init__()
        self._copyright = copyright
        self._version = version
        self._bg_two = bg_two
        self._font_family = font_family
        self._text_size = text_size
        self._text_description_color = text_description_color
        self._radius = radius
        self._padding = padding
        self.setup_ui()

    def setup_ui(self):
        self.widget_layout = qtw.QHBoxLayout(self)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)

        style = f"""
        #bg_frame {{
            border-radius: {self._radius}px;
            background-color: {self._bg_two};
        }}
        QLabel {{
            font: {self._text_size}pt "{self._font_family}";
            color: {self._text_description_color};
            padding-left: {self._padding}px;
            padding-right: {self._padding}px;
        }}
        """

        self.bg_frame = qtw.QFrame()
        self.bg_frame.setObjectName("bg_frame")
        self.bg_frame.setStyleSheet(style)

        self.widget_layout.addWidget(self.bg_frame)

        self.bg_layout = qtw.QHBoxLayout(self.bg_frame)
        self.bg_layout.setContentsMargins(0, 0, 0, 0)

        self.copyright_label = qtw.QLabel(self._copyright)
        self.copyright_label.setAlignment(qtc.Qt.AlignVCenter)

        self.version_label = qtw.QLabel(self._version)
        self.version_label.setAlignment(qtc.Qt.AlignVCenter)

        self.separator = qtw.QSpacerItem(
            20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum
        )

        self.bg_layout.addWidget(self.copyright_label)
        self.bg_layout.addSpacerItem(self.separator)
        self.bg_layout.addWidget(self.version_label)
