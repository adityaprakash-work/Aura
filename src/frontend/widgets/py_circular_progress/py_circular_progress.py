# ---INFO-----------------------------------------------------------------------
"""
PyCircularProgress widget for the application.
"""


# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw


# ---SRC------------------------------------------------------------------------
class PyCircularProgress(qtw.QWidget):
    def __init__(
        self,
        value=0,
        progress_width=10,
        is_rounded=True,
        max_value=100,
        progress_color="#ff79c6",
        enable_text=True,
        font_family="Segoe UI",
        font_size=12,
        suffix="%",
        text_color="#ff79c6",
        enable_bg=True,
        bg_color="#44475a",
    ):
        super().__init__()
        self.value = value
        self.progress_width = progress_width
        self.progress_rounded_cap = is_rounded
        self.max_value = max_value
        self.progress_color = progress_color
        self.enable_text = enable_text
        self.font_family = font_family
        self.font_size = font_size
        self.suffix = suffix
        self.text_color = text_color
        self.enable_bg = enable_bg
        self.bg_color = bg_color

    def add_shadow(self, enable):
        if enable:
            self.shadow = qtw.QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(qtg.qtg.QColor(0, 0, 0, 80))
            self.setGraphicsEffect(self.shadow)

    def set_value(self, value):
        self.value = value
        self.repaint()

    def paint_event(self, e):
        width = self.width() - self.progress_width
        height = self.height() - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value
        paint = qtg.QPainter()
        paint.begin(self)
        paint.setRenderHint(qtg.QPainter.Antialiasing)
        paint.setFont(qtg.QFont(self.font_family, self.font_size))
        rect = qtc.QRect(0, 0, self.width(), self.height())
        paint.setPen(qtc.Qt.NoPen)
        pen = qtg.QPen()
        pen.setWidth(self.progress_width)

        if self.progress_rounded_cap:
            pen.setCapStyle(qtc.Qt.RoundCap)

        if self.enable_bg:
            pen.setColor(qtg.QColor(self.bg_color))
            paint.setPen(pen)
            paint.drawArc(margin, margin, width, height, 0, 360 * 16)

        pen.setColor(qtg.QColor(self.progress_color))
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)

        if self.enable_text:
            pen.setColor(qtg.QColor(self.text_color))
            paint.setPen(pen)
            paint.drawText(
                rect,
                qtc.Qt.AlignCenter,
                f"{self.value}{self.suffix}",
            )
        paint.end()
