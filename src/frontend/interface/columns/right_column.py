# ---INFO-----------------------------------------------------------------------
"""
Right Column of the main window.
"""

# ---DEPENDENCIES---------------------------------------------------------------
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw


# ---SRC------------------------------------------------------------------------
class UIRightColumn:
    def setup_ui(self, RightColumn):
        if not RightColumn.objectName():
            RightColumn.setObjectName("RightColumn")
        RightColumn.resize(240, 600)
        self.main_pages_layout = qtw.QVBoxLayout(RightColumn)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName("main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.menus = qtw.QStackedWidget(RightColumn)
        self.menus.setObjectName("menus")
        self.menu_1 = qtw.QWidget()
        self.menu_1.setObjectName("menu_1")
        self.verticalLayout = qtw.QVBoxLayout(self.menu_1)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.btn_1_widget = qtw.QWidget(self.menu_1)
        self.btn_1_widget.setObjectName("btn_1_widget")
        self.btn_1_widget.setMinimumSize(qtc.QSize(0, 40))
        self.btn_1_widget.setMaximumSize(qtc.QSize(16777215, 40))
        self.btn_1_layout = qtw.QVBoxLayout(self.btn_1_widget)
        self.btn_1_layout.setSpacing(0)
        self.btn_1_layout.setObjectName("btn_1_layout")
        self.btn_1_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.btn_1_widget)

        self.label_1 = qtw.QLabel(self.menu_1)
        self.label_1.setObjectName("label_1")
        font = qtg.QFont()
        font.setPointSize(16)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet("font-size: 16pt")
        self.label_1.setAlignment(qtc.Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_1)

        self.menus.addWidget(self.menu_1)
        self.menu_2 = qtw.QWidget()
        self.menu_2.setObjectName("menu_2")
        self.verticalLayout_2 = qtw.QVBoxLayout(self.menu_2)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.btn_2_widget = qtw.QWidget(self.menu_2)
        self.btn_2_widget.setObjectName("btn_2_widget")
        self.btn_2_widget.setMinimumSize(qtc.QSize(0, 40))
        self.btn_2_widget.setMaximumSize(qtc.QSize(16777215, 40))
        self.btn_2_layout = qtw.QVBoxLayout(self.btn_2_widget)
        self.btn_2_layout.setSpacing(0)
        self.btn_2_layout.setObjectName("btn_2_layout")
        self.btn_2_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.btn_2_widget)

        self.label_2 = qtw.QLabel(self.menu_2)
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("font-size: 16pt")
        self.label_2.setAlignment(qtc.Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = qtw.QLabel(self.menu_2)
        self.label_3.setObjectName("label_3")
        font1 = qtg.QFont()
        font1.setPointSize(9)
        self.label_3.setFont(font1)
        self.label_3.setStyleSheet("font-size: 9pt")
        self.label_3.setAlignment(qtc.Qt.AlignCenter)
        self.label_3.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_3)

        self.menus.addWidget(self.menu_2)
        self.main_pages_layout.addWidget(self.menus)
        self.retranslate_ui(RightColumn)
        self.menus.setCurrentIndex(1)

        qtc.QMetaObject.connectSlotsByName(RightColumn)

    def retranslate_ui(self, RightColumn):
        RightColumn.setWindowTitle(
            qtc.QCoreApplication.translate(
                "RightColumn",
                "Form",
                None,
            )
        )
        self.label_1.setText(
            qtc.QCoreApplication.translate(
                "RightColumn",
                "Menu 1 - Right Menu",
                None,
            )
        )
        self.label_2.setText(
            qtc.QCoreApplication.translate(
                "RightColumn",
                "Menu 2 - Right Menu",
                None,
            )
        )
        self.label_3.setText(
            qtc.QCoreApplication.translate(
                "RightColumn",
                "This is just an example menu.\n"
                "Add Qt Widgets or your custom widgets here.",
                None,
            )
        )
