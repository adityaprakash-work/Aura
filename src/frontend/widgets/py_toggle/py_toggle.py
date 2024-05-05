# ---INFO-----------------------------------------------------------------------
"""
PyToggle widget for the application.
"""


# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw


# ---SRC------------------------------------------------------------------------
class PyToggle(qtw.QCheckBox):
    def __init__(
        self,
        width=50,
        bg_color="#777",
        circle_color="#DDD",
        active_color="#00BCFF",
        animation_curve=qtc.QEasingCurve.OutBounce,
    ):
        super().__init__()
        self.setFixedSize(width, 28)
        self.setCursor(qtc.Qt.PointingHandCursor)

        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        self._position = 3
        self.animation = qtc.QPropertyAnimation(self, b"position")
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)
        self.stateChanged.connect(self.setup_animation)

    @qtc.Property(float)
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos
        self.update()

    def setup_animation(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(4)
        self.animation.start()

    def hitButton(self, pos: qtc.QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = qtg.QPainter(self)
        p.setRenderHint(qtg.QPainter.Antialiasing)
        p.setFont(qtg.QFont("Segoe UI", 9))
        p.setPen(qtc.Qt.NoPen)

        rect = qtc.QRect(0, 0, self.width(), self.height())

        if not self.isChecked():
            p.setBrush(qtg.QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
            p.setBrush(qtg.QColor(self._circle_color))
            p.drawEllipse(self._position, 3, 22, 22)
        else:
            p.setBrush(qtg.QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
            p.setBrush(qtg.QColor(self._circle_color))
            p.drawEllipse(self._position, 3, 22, 22)

        p.end()
