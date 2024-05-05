# ---INFO-----------------------------------------------------------------------
"""
Main window of the application.
"""

# ---DEPENDENCIES---------------------------------------------------------------
import os
import sys
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from frontend.core import assets, settings
from frontend.interface.windows import main_window as mwin

os.environ["QT_FONT_DPI"] = "96"
# TODO: Add a facility to set the scale factor in the UI.
# os.environ["QT_SCALE_FACTOR"] = "2"


# ---SRC------------------------------------------------------------------------
class MainWindow(qtw.QMainWindow):
    def __init__(self, custom_settings=None):
        super().__init__()
        self.ui = mwin.UIMainWindow()
        self.ui.setup_ui(self)

        if custom_settings is not None:
            self.settings = custom_settings
        else:
            self.settings = settings.DEFAULT_FRONTEND_SETTINGS

        self.hide_grips = True
        mwin.SetupMainWindow.setup_gui(self)

        self.show()

    def btn_clicked(self):
        btn = mwin.SetupMainWindow.setup_btns(self)

        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        top_settings = mwin.MainFunctions.get_title_bar_btn(
            self,
            "btn_top_settings",
        )
        top_settings.set_active(False)

        if btn.objectName() == "btn_home":
            self.ui.left_menu.select_only_one(btn.objectName())
            mwin.MainFunctions.set_page(self, self.ui.load_pages.page_1)

        if btn.objectName() == "btn_widgets":
            self.ui.left_menu.select_only_one(btn.objectName())
            mwin.MainFunctions.set_page(self, self.ui.load_pages.page_2)

        if btn.objectName() == "btn_add_user":
            self.ui.left_menu.select_only_one(btn.objectName())
            mwin.MainFunctions.set_page(self, self.ui.load_pages.page_3)

        if btn.objectName() == "btn_info":
            if not mwin.MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())
                mwin.MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    mwin.MainFunctions.toggle_left_column(self)

                self.ui.left_menu.select_only_one_tab(btn.objectName())

            if btn.objectName() != "btn_close_left_column":
                mwin.MainFunctions.set_left_column_menu(
                    self,
                    menu=self.ui.left_column.menus.menu_2,
                    title="Info tab",
                    icon_path=assets.set_svg_ico("icon_info.svg"),
                )

        if (
            btn.objectName() == "btn_settings"
            or btn.objectName() == "btn_close_left_column"
        ):
            if not mwin.MainFunctions.left_column_is_visible(self):
                mwin.MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    mwin.MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            if btn.objectName() != "btn_close_left_column":
                mwin.MainFunctions.set_left_column_menu(
                    self,
                    menu=self.ui.left_column.menus.menu_1,
                    title="Settings Left Column",
                    icon_path=assets.set_svg_ico("icon_settings.svg"),
                )

        if btn.objectName() == "btn_top_settings":
            if not mwin.MainFunctions.right_column_is_visible(self):
                btn.set_active(True)
                mwin.MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)
                mwin.MainFunctions.toggle_right_column(self)

            top_settings = mwin.MainFunctions.get_left_menu_btn(
                self,
                "btn_settings",
            )
            top_settings.set_active_tab(False)

        print(f"Button {btn.objectName()}, clicked!")

    def btn_released(self):
        btn = mwin.SetupMainWindow.setup_btns(self)
        # NOTE: Debugging purposes.
        print(f"Button {btn.objectName()}, released!")

    def resizeEvent(self, event):
        mwin.SetupMainWindow.resize_grips(self)

    def mousePressEvent(self, event):
        # self.dragPos = event.globalPos()
        self.dragPos = event.globalPosition().toPoint()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    app.setWindowIcon(qtg.QIcon(assets.set_app_ico()))
    window = MainWindow()
    sys.exit(app.exec())
