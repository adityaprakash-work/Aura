# ---INFO-----------------------------------------------------------------------
"""
Main window functions for the application.
"""


# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
from .ui_main import UIMainWindow


# ---SRC------------------------------------------------------------------------
class MainFunctions:
    def __init__(self):
        self.ui = UIMainWindow()
        self.ui.setup_ui(self)

    def set_page(self, page):
        self.ui.load_pages.pages.setCurrentWidget(page)

    def set_left_column_menu(self, menu, title, icon_path):
        self.ui.left_column.menus.menus.setCurrentWidget(menu)
        self.ui.left_column.title_label.setText(title)
        self.ui.left_column.icon.set_icon(icon_path)

    def left_column_is_visible(self):
        width = self.ui.left_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    def right_column_is_visible(self):
        width = self.ui.right_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    def set_right_column_menu(self, menu):
        self.ui.right_column.menus.setCurrentWidget(menu)

    def get_title_bar_btn(self, object_name):
        return self.ui.title_bar_frame.findChild(qtw.QPushButton, object_name)

    def get_left_menu_btn(self, object_name):
        return self.ui.left_menu.findChild(qtw.QPushButton, object_name)

    def toggle_left_column(self):
        width = self.ui.left_column_frame.width()
        right_column_width = self.ui.right_column_frame.width()
        MainFunctions.start_box_animation(
            self,
            width,
            right_column_width,
            "left",
        )

    def toggle_right_column(self):
        left_column_width = self.ui.left_column_frame.width()
        width = self.ui.right_column_frame.width()
        MainFunctions.start_box_animation(
            self,
            left_column_width,
            width,
            "right",
        )

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0
        time_animation = self.ui.settings.time_animation
        minimum_left = self.ui.settings.left_column_size["minimum"]
        maximum_left = self.ui.settings.left_column_size["maximum"]
        minimum_right = self.ui.settings.right_column_size["minimum"]
        maximum_right = self.ui.settings.right_column_size["maximum"]

        left_width = (
            maximum_left
            if left_box_width == minimum_left and direction == "left"
            else minimum_left
        )

        right_width = (
            maximum_right
            if right_box_width == minimum_right and direction == "right"
            else minimum_right
        )

        self.left_box = qtc.QPropertyAnimation(
            self.ui.left_column_frame,
            b"minimumWidth",
        )
        self.left_box.setDuration(time_animation)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(qtc.QEasingCurve.InOutQuart)

        self.right_box = qtc.QPropertyAnimation(
            self.ui.right_column_frame,
            b"minimumWidth",
        )
        self.right_box.setDuration(time_animation)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(qtc.QEasingCurve.InOutQuart)

        self.group = qtc.QParallelAnimationGroup()
        self.group.stop()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()
