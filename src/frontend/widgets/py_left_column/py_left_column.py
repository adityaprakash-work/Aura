# ---INFO-----------------------------------------------------------------------
"""
PyLeftColumn widget for the application.
"""


# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
from .py_icon import PyIcon
from .py_left_button import PyLeftButton
from ...interface.columns.left_column import UILeftColumn


# ---SRC------------------------------------------------------------------------
class PyLeftColumn(qtw.QWidget):
    clicked = qtc.Signal(object)
    released = qtc.Signal(object)

    def __init__(
        self,
        parent,
        app_parent,
        text_title,
        text_title_size,
        text_title_color,
        dark_one,
        bg_color,
        btn_color,
        btn_color_hover,
        btn_color_pressed,
        icon_path,
        icon_color,
        icon_color_hover,
        icon_color_pressed,
        context_color,
        icon_close_path,
        radius=8,
    ):
        super().__init__()

        self._parent = parent
        self._app_parent = app_parent
        self._text_title = text_title
        self._text_title_size = text_title_size
        self._text_title_color = text_title_color
        self._icon_path = icon_path
        self._dark_one = dark_one
        self._bg_color = bg_color
        self._btn_color = btn_color
        self._btn_color_hover = btn_color_hover
        self._btn_color_pressed = btn_color_pressed
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._context_color = context_color
        self._icon_close_path = icon_close_path
        self._radius = radius

        self.setup_ui()

        self.menus = UILeftColumn()
        self.menus.setup_ui(self.content_frame)

        self.btn_close.clicked.connect(self.btn_clicked)
        self.btn_close.released.connect(self.btn_released)

    def btn_clicked(self):
        self.clicked.emit(self.btn_close)

    def btn_released(self):
        self.released.emit(self.btn_close)

    def setup_ui(self):
        self.base_layout = qtw.QVBoxLayout(self)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setSpacing(0)

        self.title_frame = qtw.QFrame()
        self.title_frame.setMaximumHeight(47)
        self.title_frame.setMinimumHeight(47)

        self.title_base_layout = qtw.QVBoxLayout(self.title_frame)
        self.title_base_layout.setContentsMargins(5, 3, 5, 3)

        self.title_bg_frame = qtw.QFrame()
        self.title_bg_frame.setObjectName("title_bg_frame")
        self.title_bg_frame.setStyleSheet(
            f"""
        #title_bg_frame {{
            background-color: {self._bg_color};
            border-radius: {self._radius}px;
        }}
        """
        )

        self.title_bg_layout = qtw.QHBoxLayout(self.title_bg_frame)
        self.title_bg_layout.setContentsMargins(5, 5, 5, 5)
        self.title_bg_layout.setSpacing(3)

        self.icon_frame = qtw.QFrame()
        self.icon_frame.setFixedSize(30, 30)
        self.icon_frame.setStyleSheet("background: none;")
        self.icon_layout = qtw.QVBoxLayout(self.icon_frame)
        self.icon_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_layout.setSpacing(5)
        self.icon = PyIcon(self._icon_path, self._icon_color)
        self.icon_layout.addWidget(
            self.icon,
            qtc.Qt.AlignCenter,
            qtc.Qt.AlignCenter,
        )

        self.title_label = qtw.QLabel(self._text_title)
        self.title_label.setObjectName("title_label")
        self.title_label.setStyleSheet(
            f"""
        #title_label {{
            font-size: {self._text_title_size}pt;
            color: {self._text_title_color};
            padding-bottom: 2px;
            background: none;
        }}
        """
        )

        self.btn_frame = qtw.QFrame()
        self.btn_frame.setFixedSize(30, 30)
        self.btn_frame.setStyleSheet("background: none;")
        self.btn_close = PyLeftButton(
            self._parent,
            self._app_parent,
            tooltip_text="Hide",
            dark_one=self._dark_one,
            bg_color=self._btn_color,
            bg_color_hover=self._btn_color_hover,
            bg_color_pressed=self._btn_color_pressed,
            icon_color=self._icon_color,
            icon_color_hover=self._icon_color_hover,
            icon_color_pressed=self._icon_color_pressed,
            icon_color_active=self._icon_color_pressed,
            context_color=self._context_color,
            text_foreground=self._text_title_color,
            icon_path=self._icon_close_path,
            radius=6,
        )
        self.btn_close.setParent(self.btn_frame)
        self.btn_close.setObjectName("btn_close_left_column")

        self.title_bg_layout.addWidget(self.icon_frame)
        self.title_bg_layout.addWidget(self.title_label)
        self.title_bg_layout.addWidget(self.btn_frame)

        self.title_base_layout.addWidget(self.title_bg_frame)

        self.content_frame = qtw.QFrame()
        self.content_frame.setStyleSheet("background: none")

        self.base_layout.addWidget(self.title_frame)
        self.base_layout.addWidget(self.content_frame)
