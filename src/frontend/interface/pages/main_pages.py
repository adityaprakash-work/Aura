# ---INFO-----------------------------------------------------------------------
"""
Main Pages of the main window.
"""

__all__ = [
    "UIMainPages",
]


# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw


# ---SRC------------------------------------------------------------------------
class UIMainPages:
    def setup_ui(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName("MainPages")
        MainPages.resize(860, 600)
        self.main_pages_layout = qtw.QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName("main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = qtw.QStackedWidget(MainPages)
        self.pages.setObjectName("pages")
        self.page_1 = qtw.QWidget()
        self.page_1.setObjectName("page_1")
        self.page_1.setStyleSheet("font-size: 14pt")
        self.page_1_layout = qtw.QVBoxLayout(self.page_1)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName("page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.welcome_base = qtw.QFrame(self.page_1)
        self.welcome_base.setObjectName("welcome_base")
        self.welcome_base.setMinimumSize(qtc.QSize(300, 150))
        self.welcome_base.setMaximumSize(qtc.QSize(300, 150))
        self.welcome_base.setFrameShape(qtw.QFrame.NoFrame)
        self.welcome_base.setFrameShadow(qtw.QFrame.Raised)
        self.center_page_layout = qtw.QVBoxLayout(self.welcome_base)
        self.center_page_layout.setSpacing(10)
        self.center_page_layout.setObjectName("center_page_layout")
        self.center_page_layout.setContentsMargins(0, 0, 0, 0)
        self.logo = qtw.QFrame(self.welcome_base)
        self.logo.setObjectName("logo")
        self.logo.setMinimumSize(qtc.QSize(300, 120))
        self.logo.setMaximumSize(qtc.QSize(300, 120))
        self.logo.setFrameShape(qtw.QFrame.NoFrame)
        self.logo.setFrameShadow(qtw.QFrame.Raised)
        self.logo_layout = qtw.QVBoxLayout(self.logo)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName("logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        self.center_page_layout.addWidget(self.logo)

        self.label = qtw.QLabel(self.welcome_base)
        self.label.setObjectName("label")
        self.label.setAlignment(qtc.Qt.AlignCenter)

        self.center_page_layout.addWidget(self.label)

        self.page_1_layout.addWidget(self.welcome_base, 0, qtc.Qt.AlignHCenter)

        self.pages.addWidget(self.page_1)
        self.page_2 = qtw.QWidget()
        self.page_2.setObjectName("page_2")
        self.page_2_layout = qtw.QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName("page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area = qtw.QScrollArea(self.page_2)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setStyleSheet("background: transparent;")
        self.scroll_area.setFrameShape(qtw.QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.contents = qtw.QWidget()
        self.contents.setObjectName("contents")
        self.contents.setGeometry(qtc.QRect(0, 0, 840, 580))
        self.contents.setStyleSheet("background: transparent;")
        self.verticalLayout = qtw.QVBoxLayout(self.contents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.title_label = qtw.QLabel(self.contents)
        self.title_label.setObjectName("title_label")
        self.title_label.setMaximumSize(qtc.QSize(16777215, 40))
        font = qtg.QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("font-size: 16pt")
        self.title_label.setAlignment(qtc.Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title_label)

        self.description_label = qtw.QLabel(self.contents)
        self.description_label.setObjectName("description_label")
        description_label_alignment = qtc.Qt.AlignHCenter | qtc.Qt.AlignTop
        self.description_label.setAlignment(description_label_alignment)
        self.description_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.description_label)

        self.row_1_layout = qtw.QHBoxLayout()
        self.row_1_layout.setObjectName("row_1_layout")

        self.verticalLayout.addLayout(self.row_1_layout)

        self.row_2_layout = qtw.QHBoxLayout()
        self.row_2_layout.setObjectName("row_2_layout")

        self.verticalLayout.addLayout(self.row_2_layout)

        self.row_3_layout = qtw.QHBoxLayout()
        self.row_3_layout.setObjectName("row_3_layout")

        self.verticalLayout.addLayout(self.row_3_layout)

        self.row_4_layout = qtw.QVBoxLayout()
        self.row_4_layout.setObjectName("row_4_layout")

        self.verticalLayout.addLayout(self.row_4_layout)

        self.row_5_layout = qtw.QVBoxLayout()
        self.row_5_layout.setObjectName("row_5_layout")

        self.verticalLayout.addLayout(self.row_5_layout)
        self.scroll_area.setWidget(self.contents)
        self.page_2_layout.addWidget(self.scroll_area)

        self.pages.addWidget(self.page_2)
        self.page_3 = qtw.QWidget()
        self.page_3.setObjectName("page_3")
        self.page_3.setStyleSheet("QFrame { font-size: 16pt; }")
        self.page_3_layout = qtw.QVBoxLayout(self.page_3)
        self.page_3_layout.setObjectName("page_3_layout")
        self.empty_page_label = qtw.QLabel(self.page_3)
        self.empty_page_label.setObjectName("empty_page_label")
        self.empty_page_label.setFont(font)
        self.empty_page_label.setAlignment(qtc.Qt.AlignCenter)

        self.page_3_layout.addWidget(self.empty_page_label)
        self.pages.addWidget(self.page_3)
        self.main_pages_layout.addWidget(self.pages)
        self.retranslate_ui(MainPages)
        self.pages.setCurrentIndex(0)

        qtc.QMetaObject.connectSlotsByName(MainPages)

    def retranslate_ui(self, MainPages):
        MainPages.setWindowTitle(
            qtc.QCoreApplication.translate(
                "MainPages",
                "Form",
                None,
            )
        )
        self.label.setText(
            qtc.QCoreApplication.translate(
                "MainPages",
                "Welcome To PyOneDark GUI",
                None,
            )
        )
        self.title_label.setText(
            qtc.QCoreApplication.translate(
                "MainPages",
                "Custom Widgets Page",
                None,
            )
        )
        self.description_label.setText(
            qtc.QCoreApplication.translate(
                "MainPages",
                (
                    "Here will be all the custom widgets, they will be added "
                    "over time on this page.\n"
                    "I will try to always record a new tutorial when adding a "
                    "new Widget and updating the project on Patreon before "
                    "launching on GitHub and GitHub after the public release."
                ),
                None,
            )
        )
        self.empty_page_label.setText(
            qtc.QCoreApplication.translate(
                "MainPages",
                "Empty Page",
                None,
            )
        )
