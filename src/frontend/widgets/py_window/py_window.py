# ---INFO-----------------------------------------------------------------------
"""
PyWindow widget for the application.
"""


# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw

from .styles import Styles
from ...core import settings


# ---SRC------------------------------------------------------------------------
class PyWindow(qtw.QFrame):
    def __init__(
        self,
        parent,
        layout=qtc.Qt.Vertical,
        margin=0,
        spacing=2,
        bg_color="#2c313c",
        text_color="#fff",
        text_font="9pt 'Segoe UI'",
        border_radius=10,
        border_size=2,
        border_color="#343b48",
        enable_shadow=True,
        custom_settings=None,
    ):
        super().__init__()
        if custom_settings is not None:
            self.settings = custom_settings
        else:
            self.settings = settings.DEFAULT_FRONTEND_SETTINGS

        self.parent = parent
        self.layout = layout
        self.margin = margin
        self.bg_color = bg_color
        self.text_color = text_color
        self.text_font = text_font
        self.border_radius = border_radius
        self.border_size = border_size
        self.border_color = border_color
        self.enable_shadow = enable_shadow

        self.setObjectName("aura_bg_app")
        self.set_stylesheet()

        if layout == qtc.Qt.Vertical:
            self.layout = qtw.QHBoxLayout(self)
        else:
            self.layout = qtw.QHBoxLayout(self)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.layout.setSpacing(spacing)

        if self.settings.custom_title_bar:
            if enable_shadow:
                self.shadow = qtw.QGraphicsDropShadowEffect()
                self.shadow.setBlurRadius(20)
                self.shadow.setXOffset(0)
                self.shadow.setYOffset(0)
                self.shadow.setColor(qtg.QColor(0, 0, 0, 160))
                self.setGraphicsEffect(self.shadow)

    def set_stylesheet(
        self,
        bg_color=None,
        border_radius=None,
        border_size=None,
        border_color=None,
        text_color=None,
        text_font=None,
    ):
        internal_bg_color = bg_color or self.bg_color
        internal_border_radius = border_radius or self.border_radius
        internal_border_size = border_size or self.border_size
        internal_text_color = text_color or self.text_color
        internal_border_color = border_color or self.border_color
        internal_text_font = text_font or self.text_font

        self.setStyleSheet(
            Styles.bg_style.format(
                _bg_color=internal_bg_color,
                _border_radius=internal_border_radius,
                _border_size=internal_border_size,
                _border_color=internal_border_color,
                _text_color=internal_text_color,
                _text_font=internal_text_font,
            )
        )
