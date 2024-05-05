# ---INFO-----------------------------------------------------------------------
"""
PyWindow widget for the application.
"""


# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
import PySide6.QtSvgWidgets as qts

from .... import widgets
from ....core import settings, themes, assets
from .functions_main_window import MainFunctions
from .ui_main import UIMainWindow


# ---SRC------------------------------------------------------------------------
class SetupMainWindow:
    def __init__(self):
        self.ui = UIMainWindow()
        self.ui.setup_ui(self)

    add_left_menus = [
        {
            "btn_icon": "icon_home.svg",
            "btn_id": "btn_home",
            "btn_text": "Home",
            "btn_tooltip": "Home page",
            "show_top": True,
            "is_active": True,
        },
        {
            "btn_icon": "icon_widgets.svg",
            "btn_id": "btn_widgets",
            "btn_text": "Show Custom Widgets",
            "btn_tooltip": "Show custom widgets",
            "show_top": True,
            "is_active": False,
        },
        {
            "btn_icon": "icon_add_user.svg",
            "btn_id": "btn_add_user",
            "btn_text": "Add Users",
            "btn_tooltip": "Add users",
            "show_top": True,
            "is_active": False,
        },
        {
            "btn_icon": "icon_file.svg",
            "btn_id": "btn_new_file",
            "btn_text": "New File",
            "btn_tooltip": "Create new file",
            "show_top": True,
            "is_active": False,
        },
        {
            "btn_icon": "icon_folder_open.svg",
            "btn_id": "btn_open_file",
            "btn_text": "Open File",
            "btn_tooltip": "Open file",
            "show_top": True,
            "is_active": False,
        },
        {
            "btn_icon": "icon_save.svg",
            "btn_id": "btn_save",
            "btn_text": "Save File",
            "btn_tooltip": "Save file",
            "show_top": True,
            "is_active": False,
        },
        {
            "btn_icon": "icon_info.svg",
            "btn_id": "btn_info",
            "btn_text": "Information",
            "btn_tooltip": "Open informations",
            "show_top": False,
            "is_active": False,
        },
        {
            "btn_icon": "icon_settings.svg",
            "btn_id": "btn_settings",
            "btn_text": "Settings",
            "btn_tooltip": "Open settings",
            "show_top": False,
            "is_active": False,
        },
    ]

    add_title_bar_menus = [
        {
            "btn_icon": "icon_search.svg",
            "btn_id": "btn_search",
            "btn_tooltip": "Search",
            "is_active": False,
        },
        {
            "btn_icon": "icon_settings.svg",
            "btn_id": "btn_top_settings",
            "btn_tooltip": "Top settings",
            "is_active": False,
        },
    ]

    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()

    def setup_gui(self, custom_settings=None, custom_theme=None):
        self.setWindowTitle(self.settings.app_name)

        if self.settings.custom_title_bar:
            self.setWindowFlag(qtc.Qt.FramelessWindowHint)
            # NOTE: This line is making the background disappear, but disabling
            # it doesn't give a smooth border either.
            self.setAttribute(qtc.Qt.WA_TranslucentBackground)

        if self.settings.custom_title_bar:
            self.left_grip = widgets.PyGrips(self, "left", self.hide_grips)
            self.right_grip = widgets.PyGrips(self, "right", self.hide_grips)
            self.top_grip = widgets.PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = widgets.PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = widgets.PyGrips(
                self,
                "top_left",
                self.hide_grips,
            )
            self.top_right_grip = widgets.PyGrips(
                self,
                "top_right",
                self.hide_grips,
            )
            self.bottom_left_grip = widgets.PyGrips(
                self, "bottom_left", self.hide_grips
            )
            self.bottom_right_grip = widgets.PyGrips(
                self, "bottom_right", self.hide_grips
            )

        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        if self.settings.custom_title_bar:
            self.ui.title_bar.set_title(self.settings.app_name)
        else:
            self.ui.title_bar.set_title("Welcome to Aura")

        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        MainFunctions.set_page(self, self.ui.load_pages.page_1)
        MainFunctions.set_left_column_menu(
            self,
            menu=self.ui.left_column.menus.menu_1,
            title="Settings Left Column",
            icon_path=assets.set_svg_ico("icon_settings.svg"),
        )
        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # NOTE: I have no clue why the original source-code has this block
        # of code here. Why reset the settings and themes?
        if custom_settings is not None:
            self.settings = custom_settings
        else:
            self.settings = settings.DEFAULT_FRONTEND_SETTINGS

        if custom_theme is not None:
            self.themes = custom_theme
        else:
            self.themes = themes.DEFAULT_FRONTEND_THEME

        self.left_btn_1 = widgets.PyPushButton(
            text="Btn 1",
            radius=8,
            color=self.themes.app_color.text_foreground,
            bg_color=self.themes.app_color.dark_one,
            bg_color_hover=self.themes.app_color.dark_three,
            bg_color_pressed=self.themes.app_color.dark_four,
        )
        self.left_btn_1.setMaximumHeight(40)
        self.ui.left_column.menus.btn_1_layout.addWidget(self.left_btn_1)

        self.left_btn_2 = widgets.PyPushButton(
            text="Btn With Icon",
            radius=8,
            color=self.themes.app_color.text_foreground,
            bg_color=self.themes.app_color.dark_one,
            bg_color_hover=self.themes.app_color.dark_three,
            bg_color_pressed=self.themes.app_color.dark_four,
        )
        self.icon = qtg.QIcon(assets.set_svg_ico("icon_settings.svg"))
        self.left_btn_2.setIcon(self.icon)
        self.left_btn_2.setMaximumHeight(40)
        self.ui.left_column.menus.btn_2_layout.addWidget(self.left_btn_2)

        self.left_btn_3 = qtw.QPushButton("Default QPushButton")
        self.left_btn_3.setMaximumHeight(40)
        self.ui.left_column.menus.btn_3_layout.addWidget(self.left_btn_3)

        self.logo_svg = qts.QSvgWidget(assets.set_svg_img("logo_home.svg"))
        self.ui.load_pages.logo_layout.addWidget(
            self.logo_svg, qtc.Qt.AlignCenter, qtc.Qt.AlignCenter
        )

        self.circular_progress_1 = widgets.PyCircularProgress(
            value=80,
            progress_color=self.themes.app_color.context_color,
            text_color=self.themes.app_color.text_title,
            font_size=14,
            bg_color=self.themes.app_color.dark_four,
        )
        self.circular_progress_1.setFixedSize(200, 200)

        self.circular_progress_2 = widgets.PyCircularProgress(
            value=45,
            progress_width=4,
            progress_color=self.themes.app_color.context_color,
            text_color=self.themes.app_color.context_color,
            font_size=14,
            bg_color=self.themes.app_color.bg_three,
        )
        self.circular_progress_2.setFixedSize(160, 160)

        self.circular_progress_3 = widgets.PyCircularProgress(
            value=75,
            progress_width=2,
            progress_color=self.themes.app_color.pink,
            text_color=self.themes.app_color.white,
            font_size=14,
            bg_color=self.themes.app_color.bg_three,
        )
        self.circular_progress_3.setFixedSize(140, 140)

        self.vertical_slider_1 = widgets.PySlider(
            margin=8,
            bg_size=10,
            bg_radius=5,
            handle_margin=-3,
            handle_size=16,
            handle_radius=8,
            bg_color=self.themes.app_color.dark_three,
            bg_color_hover=self.themes.app_color.dark_four,
            handle_color=self.themes.app_color.context_color,
            handle_color_hover=self.themes.app_color.context_hover,
            handle_color_pressed=self.themes.app_color.context_pressed,
        )
        self.vertical_slider_1.setMinimumHeight(100)

        self.vertical_slider_2 = widgets.PySlider(
            bg_color=self.themes.app_color.dark_three,
            bg_color_hover=self.themes.app_color.dark_three,
            handle_color=self.themes.app_color.context_color,
            handle_color_hover=self.themes.app_color.context_hover,
            handle_color_pressed=self.themes.app_color.context_pressed,
        )
        self.vertical_slider_2.setMinimumHeight(100)

        self.vertical_slider_3 = widgets.PySlider(
            margin=8,
            bg_size=10,
            bg_radius=5,
            handle_margin=-3,
            handle_size=16,
            handle_radius=8,
            bg_color=self.themes.app_color.dark_three,
            bg_color_hover=self.themes.app_color.dark_four,
            handle_color=self.themes.app_color.context_color,
            handle_color_hover=self.themes.app_color.context_hover,
            handle_color_pressed=self.themes.app_color.context_pressed,
        )
        self.vertical_slider_3.setOrientation(qtc.Qt.Horizontal)
        self.vertical_slider_3.setMaximumWidth(200)

        self.vertical_slider_4 = widgets.PySlider(
            bg_color=self.themes.app_color.dark_three,
            bg_color_hover=self.themes.app_color.dark_three,
            handle_color=self.themes.app_color.context_color,
            handle_color_hover=self.themes.app_color.context_hover,
            handle_color_pressed=self.themes.app_color.context_pressed,
        )
        self.vertical_slider_4.setOrientation(qtc.Qt.Horizontal)
        self.vertical_slider_4.setMaximumWidth(200)

        self.icon_button_1 = widgets.PyIconButton(
            icon_path=assets.set_svg_ico("icon_heart.svg"),
            parent=self,
            app_parent=self.ui.central_widget,
            tooltip_text="Icon button - Heart",
            width=40,
            height=40,
            radius=20,
            dark_one=self.themes.app_color.dark_one,
            icon_color=self.themes.app_color.icon_color,
            icon_color_hover=self.themes.app_color.icon_hover,
            icon_color_pressed=self.themes.app_color.icon_pressed,
            icon_color_active=self.themes.app_color.icon_active,
            bg_color=self.themes.app_color.dark_one,
            bg_color_hover=self.themes.app_color.dark_three,
            bg_color_pressed=self.themes.app_color.pink,
        )

        self.icon_button_2 = widgets.PyIconButton(
            icon_path=assets.set_svg_ico("icon_add_user.svg"),
            parent=self,
            app_parent=self.ui.central_widget,
            tooltip_text="BTN with tooltip",
            width=40,
            height=40,
            radius=8,
            dark_one=self.themes.app_color.dark_one,
            icon_color=self.themes.app_color.icon_color,
            icon_color_hover=self.themes.app_color.icon_hover,
            icon_color_pressed=self.themes.app_color.white,
            icon_color_active=self.themes.app_color.icon_active,
            bg_color=self.themes.app_color.dark_one,
            bg_color_hover=self.themes.app_color.dark_three,
            bg_color_pressed=self.themes.app_color.green,
        )

        self.icon_button_3 = widgets.PyIconButton(
            icon_path=assets.set_svg_ico("icon_add_user.svg"),
            parent=self,
            app_parent=self.ui.central_widget,
            tooltip_text="BTN actived! (is_actived = True)",
            width=40,
            height=40,
            radius=8,
            dark_one=self.themes.app_color.dark_one,
            icon_color=self.themes.app_color.icon_color,
            icon_color_hover=self.themes.app_color.icon_hover,
            icon_color_pressed=self.themes.app_color.white,
            icon_color_active=self.themes.app_color.icon_active,
            bg_color=self.themes.app_color.dark_one,
            bg_color_hover=self.themes.app_color.dark_three,
            bg_color_pressed=self.themes.app_color.context_color,
            is_active=True,
        )

        self.push_button_1 = widgets.PyPushButton(
            text="Button Without Icon",
            radius=8,
            color=self.themes.app_color.text_foreground,
            bg_color=self.themes.app_color.dark_one,
            bg_color_hover=self.themes.app_color.dark_three,
            bg_color_pressed=self.themes.app_color.dark_four,
        )
        self.push_button_1.setMinimumHeight(40)

        self.push_button_2 = widgets.PyPushButton(
            text="Button With Icon",
            radius=8,
            color=self.themes.app_color.text_foreground,
            bg_color=self.themes.app_color.dark_one,
            bg_color_hover=self.themes.app_color.dark_three,
            bg_color_pressed=self.themes.app_color.dark_four,
        )
        self.icon_2 = qtg.QIcon(assets.set_svg_ico("icon_settings.svg"))
        self.push_button_2.setMinimumHeight(40)
        self.push_button_2.setIcon(self.icon_2)

        self.line_edit = widgets.PyLineEdit(
            text="",
            place_holder_text="Place holder text",
            radius=8,
            border_size=2,
            color=self.themes.app_color.text_foreground,
            selection_color=self.themes.app_color.white,
            bg_color=self.themes.app_color.dark_one,
            bg_color_active=self.themes.app_color.dark_three,
            context_color=self.themes.app_color.context_color,
        )
        self.line_edit.setMinimumHeight(30)

        self.toggle_button = widgets.PyToggle(
            width=50,
            bg_color=self.themes.app_color.dark_two,
            circle_color=self.themes.app_color.icon_color,
            active_color=self.themes.app_color.context_color,
        )

        self.table_widget = widgets.PyTableWidget(
            radius=8,
            color=self.themes.app_color.text_foreground,
            selection_color=self.themes.app_color.context_color,
            bg_color=self.themes.app_color.bg_two,
            header_horizontal_color=self.themes.app_color.dark_two,
            header_vertical_color=self.themes.app_color.bg_three,
            bottom_line_color=self.themes.app_color.bg_three,
            grid_line_color=self.themes.app_color.bg_one,
            scroll_bar_bg_color=self.themes.app_color.bg_one,
            scroll_bar_btn_color=self.themes.app_color.dark_four,
            context_color=self.themes.app_color.context_color,
        )
        self.table_widget.setColumnCount(3)
        self.table_widget.horizontalHeader().setSectionResizeMode(
            qtw.QHeaderView.Stretch,
        )
        self.table_widget.setSelectionMode(
            qtw.QAbstractItemView.ExtendedSelection,
        )
        self.table_widget.setSelectionBehavior(
            qtw.QAbstractItemView.SelectRows,
        )

        self.column_1 = qtw.QTableWidgetItem()
        self.column_1.setTextAlignment(qtc.Qt.AlignCenter)
        self.column_1.setText("NAME")

        self.column_2 = qtw.QTableWidgetItem()
        self.column_2.setTextAlignment(qtc.Qt.AlignCenter)
        self.column_2.setText("NICK")

        self.column_3 = qtw.QTableWidgetItem()
        self.column_3.setTextAlignment(qtc.Qt.AlignCenter)
        self.column_3.setText("PASS")

        self.table_widget.setHorizontalHeaderItem(0, self.column_1)
        self.table_widget.setHorizontalHeaderItem(1, self.column_2)
        self.table_widget.setHorizontalHeaderItem(2, self.column_3)

        for x in range(10):
            row_number = self.table_widget.rowCount()
            self.table_widget.insertRow(row_number)
            self.table_widget.setItem(
                row_number, 0, qtw.QTableWidgetItem(str("Wanderson"))
            )
            self.table_widget.setItem(
                row_number,
                1,
                qtw.QTableWidgetItem(str("vfx_on_fire_" + str(x))),
            )
            self.pass_text = qtw.QTableWidgetItem()
            self.pass_text.setTextAlignment(qtc.Qt.AlignCenter)
            self.pass_text.setText("12345" + str(x))
            self.table_widget.setItem(row_number, 2, self.pass_text)
            self.table_widget.setRowHeight(row_number, 22)

        self.ui.load_pages.row_1_layout.addWidget(self.circular_progress_1)
        self.ui.load_pages.row_1_layout.addWidget(self.circular_progress_2)
        self.ui.load_pages.row_1_layout.addWidget(self.circular_progress_3)
        self.ui.load_pages.row_2_layout.addWidget(self.vertical_slider_1)
        self.ui.load_pages.row_2_layout.addWidget(self.vertical_slider_2)
        self.ui.load_pages.row_2_layout.addWidget(self.vertical_slider_3)
        self.ui.load_pages.row_2_layout.addWidget(self.vertical_slider_4)
        self.ui.load_pages.row_3_layout.addWidget(self.icon_button_1)
        self.ui.load_pages.row_3_layout.addWidget(self.icon_button_2)
        self.ui.load_pages.row_3_layout.addWidget(self.icon_button_3)
        self.ui.load_pages.row_3_layout.addWidget(self.push_button_1)
        self.ui.load_pages.row_3_layout.addWidget(self.push_button_2)
        self.ui.load_pages.row_3_layout.addWidget(self.toggle_button)
        self.ui.load_pages.row_4_layout.addWidget(self.line_edit)
        self.ui.load_pages.row_5_layout.addWidget(self.table_widget)

        self.right_btn_1 = widgets.PyPushButton(
            text="Show Menu 2",
            radius=8,
            color=self.themes.app_color.text_foreground,
            bg_color=self.themes.app_color.dark_one,
            bg_color_hover=self.themes.app_color.dark_three,
            bg_color_pressed=self.themes.app_color.dark_four,
        )
        self.icon_right = qtg.QIcon(assets.set_svg_ico("icon_arrow_right.svg"))
        self.right_btn_1.setIcon(self.icon_right)
        self.right_btn_1.setMaximumHeight(40)
        self.right_btn_1.clicked.connect(
            lambda: MainFunctions.set_right_column_menu(
                self, self.ui.right_column.menu_2
            )
        )
        self.ui.right_column.btn_1_layout.addWidget(self.right_btn_1)

        self.right_btn_2 = widgets.PyPushButton(
            text="Show Menu 1",
            radius=8,
            color=self.themes.app_color.text_foreground,
            bg_color=self.themes.app_color.dark_one,
            bg_color_hover=self.themes.app_color.dark_three,
            bg_color_pressed=self.themes.app_color.dark_four,
        )
        self.icon_left = qtg.QIcon(assets.set_svg_ico("icon_arrow_left.svg"))
        self.right_btn_2.setIcon(self.icon_left)
        self.right_btn_2.setMaximumHeight(40)
        self.right_btn_2.clicked.connect(
            lambda: MainFunctions.set_right_column_menu(
                self, self.ui.right_column.menu_1
            )
        )
        self.ui.right_column.btn_2_layout.addWidget(self.right_btn_2)

    def resize_grips(self):
        if self.settings.custom_title_bar:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(
                self.width() - 15,
                10,
                10,
                self.height(),
            )
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(
                5,
                self.height() - 15,
                self.width() - 10,
                10,
            )
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(
                self.width() - 20, self.height() - 20, 15, 15
            )
