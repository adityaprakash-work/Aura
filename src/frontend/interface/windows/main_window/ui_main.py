# ---INFO-----------------------------------------------------------------------
"""
Main Window of the application.
"""


# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtWidgets as qtw

from .... import widgets
from ...pages.main_pages import UIMainPages
from ....core import assets, settings, themes
from ...columns.right_column import UIRightColumn


# ---SRC------------------------------------------------------------------------
class UIMainWindow:
    def setup_ui(self, parent, custom_settings=None, custom_theme=None):
        if not parent.objectName():
            parent.setObjectName("MainWindow")

        if custom_settings is not None:
            self.settings = custom_settings
        else:
            self.settings = settings.DEFAULT_FRONTEND_SETTINGS

        if custom_theme is not None:
            self.themes = custom_theme
        else:
            self.themes = themes.DEFAULT_FRONTEND_THEME

        parent.resize(
            self.settings.startup_size[0],
            self.settings.startup_size[1],
        )
        parent.setMinimumSize(
            self.settings.minimum_size[0],
            self.settings.minimum_size[1],
        )

        self.central_widget = qtw.QWidget()
        self.central_widget.setStyleSheet(
            f"font: {self.settings.font['text_size']}pt "
            f'"{self.settings.font['family']}"; '
            f'color: {self.themes.app_color.text_foreground};'
        )
        self.central_widget_layout = qtw.QVBoxLayout(self.central_widget)
        if self.settings.custom_title_bar:
            self.central_widget_layout.setContentsMargins(10, 10, 10, 10)
        else:
            self.central_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.window = widgets.PyWindow(
            parent,
            bg_color=self.themes.app_color.bg_one,
            border_color=self.themes.app_color.bg_two,
            text_color=self.themes.app_color.text_foreground,
        )

        if not self.settings.custom_title_bar:
            self.window.set_stylesheet(border_radius=0, border_size=0)

        self.central_widget_layout.addWidget(self.window)

        left_menu_margin = self.settings.left_menu_content_margins
        left_menu_minimum = self.settings.left_menu_size["minimum"]
        self.left_menu_frame = qtw.QFrame()
        self.left_menu_frame.setMaximumSize(
            left_menu_minimum + (left_menu_margin * 2), 17280
        )
        self.left_menu_frame.setMinimumSize(
            left_menu_minimum + (left_menu_margin * 2), 0
        )

        self.left_menu_layout = qtw.QHBoxLayout(self.left_menu_frame)
        self.left_menu_layout.setContentsMargins(
            left_menu_margin,
            left_menu_margin,
            left_menu_margin,
            left_menu_margin,
        )

        self.left_menu = widgets.PyLeftMenu(
            parent=self.left_menu_frame,
            app_parent=self.central_widget,
            dark_one=self.themes.app_color.dark_one,
            dark_three=self.themes.app_color.dark_three,
            dark_four=self.themes.app_color.dark_four,
            bg_one=self.themes.app_color.bg_one,
            icon_color=self.themes.app_color.icon_color,
            icon_color_hover=self.themes.app_color.icon_hover,
            icon_color_pressed=self.themes.app_color.icon_pressed,
            icon_color_active=self.themes.app_color.icon_active,
            context_color=self.themes.app_color.context_color,
            text_foreground=self.themes.app_color.text_foreground,
            text_active=self.themes.app_color.text_active,
        )
        self.left_menu_layout.addWidget(self.left_menu)
        self.left_column_frame = qtw.QFrame()
        self.left_column_frame.setMaximumWidth(
            self.settings.left_column_size["minimum"]
        )
        self.left_column_frame.setMinimumWidth(
            self.settings.left_column_size["minimum"]
        )
        self.left_column_frame.setStyleSheet(
            f"background: {self.themes.app_color.bg_two}"
        )

        self.left_column_layout = qtw.QVBoxLayout(self.left_column_frame)
        self.left_column_layout.setContentsMargins(0, 0, 0, 0)

        self.left_column = widgets.PyLeftColumn(
            parent,
            app_parent=self.central_widget,
            text_title="Settings Left Frame",
            text_title_size=self.settings.font["title_size"],
            text_title_color=self.themes.app_color.text_foreground,
            icon_path=assets.set_svg_ico("icon_settings.svg"),
            dark_one=self.themes.app_color.dark_one,
            bg_color=self.themes.app_color.bg_three,
            btn_color=self.themes.app_color.bg_three,
            btn_color_hover=self.themes.app_color.bg_two,
            btn_color_pressed=self.themes.app_color.bg_one,
            icon_color=self.themes.app_color.icon_color,
            icon_color_hover=self.themes.app_color.icon_hover,
            context_color=self.themes.app_color.context_color,
            icon_color_pressed=self.themes.app_color.icon_pressed,
            icon_close_path=assets.set_svg_ico("icon_close.svg"),
        )
        self.left_column_layout.addWidget(self.left_column)

        self.right_app_frame = qtw.QFrame()
        self.right_app_layout = qtw.QVBoxLayout(self.right_app_frame)
        self.right_app_layout.setContentsMargins(3, 3, 3, 3)
        self.right_app_layout.setSpacing(6)

        self.title_bar_frame = qtw.QFrame()
        self.title_bar_frame.setMinimumHeight(40)
        self.title_bar_frame.setMaximumHeight(40)
        self.title_bar_layout = qtw.QVBoxLayout(self.title_bar_frame)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.title_bar = widgets.PyTitleBar(
            parent,
            logo_width=100,
            app_parent=self.central_widget,
            logo_image="logo_top_100x22.svg",
            bg_color=self.themes.app_color.bg_two,
            div_color=self.themes.app_color.bg_three,
            btn_bg_color=self.themes.app_color.bg_two,
            btn_bg_color_hover=self.themes.app_color.bg_three,
            btn_bg_color_pressed=self.themes.app_color.bg_one,
            icon_color=self.themes.app_color.icon_color,
            icon_color_hover=self.themes.app_color.icon_hover,
            icon_color_pressed=self.themes.app_color.icon_pressed,
            icon_color_active=self.themes.app_color.icon_active,
            context_color=self.themes.app_color.context_color,
            dark_one=self.themes.app_color.dark_one,
            text_foreground=self.themes.app_color.text_foreground,
            radius=8,
            font_family=self.settings.font["family"],
            title_size=self.settings.font["title_size"],
            is_custom_title_bar=self.settings.custom_title_bar,
        )
        self.title_bar_layout.addWidget(self.title_bar)

        self.content_area_frame = qtw.QFrame()
        self.content_area_layout = qtw.QHBoxLayout(self.content_area_frame)
        self.content_area_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area_layout.setSpacing(0)
        self.content_area_left_frame = qtw.QFrame()

        self.load_pages = UIMainPages()
        self.load_pages.setup_ui(self.content_area_left_frame)

        self.right_column_frame = qtw.QFrame()
        self.right_column_frame.setMinimumWidth(
            self.settings.right_column_size["minimum"]
        )
        self.right_column_frame.setMaximumWidth(
            self.settings.right_column_size["maximum"]
        )

        self.content_area_right_layout = qtw.QVBoxLayout(
            self.right_column_frame,
        )
        self.content_area_right_layout.setContentsMargins(5, 5, 5, 5)
        self.content_area_right_layout.setSpacing(0)

        self.content_area_right_bg_frame = qtw.QFrame()
        self.content_area_right_bg_frame.setObjectName(
            "content_area_right_bg_frame",
        )
        self.content_area_right_bg_frame.setStyleSheet(
            f"""
        #content_area_right_bg_frame {{
            border-radius: 8px;
            background-color: {self.themes.app_color.bg_two};
        }}
        """
        )

        self.content_area_right_layout.addWidget(
            self.content_area_right_bg_frame,
        )

        self.right_column = UIRightColumn()
        self.right_column.setup_ui(self.content_area_right_bg_frame)

        self.content_area_layout.addWidget(self.content_area_left_frame)
        self.content_area_layout.addWidget(self.right_column_frame)

        self.credits_frame = qtw.QFrame()
        self.credits_frame.setMinimumHeight(26)
        self.credits_frame.setMaximumHeight(26)

        self.credits_layout = qtw.QVBoxLayout(self.credits_frame)
        self.credits_layout.setContentsMargins(0, 0, 0, 0)

        self.credits = widgets.PyCredits(
            bg_two=self.themes.app_color.bg_two,
            copyright=self.settings.copyright,
            version=self.settings.version,
            font_family=self.settings.font["family"],
            text_size=self.settings.font["text_size"],
            text_description_color=self.themes.app_color.text_description,
        )

        self.credits_layout.addWidget(self.credits)

        self.right_app_layout.addWidget(self.title_bar_frame)
        self.right_app_layout.addWidget(self.content_area_frame)
        self.right_app_layout.addWidget(self.credits_frame)

        self.window.layout.addWidget(self.left_menu_frame)
        self.window.layout.addWidget(self.left_column_frame)
        self.window.layout.addWidget(self.right_app_frame)

        parent.setCentralWidget(self.central_widget)
