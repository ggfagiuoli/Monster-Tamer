from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QSpacerItem, QPushButton
from PySide6.QtGui import QFont, QResizeEvent
from PySide6.QtCore import QSize, Qt, Signal
from typing import Self
from src.helper import subWidget, ORIENTATION
from src.request_button import RequestButton
from src.requesters import StubLoginRequester
from src.body_getters import BodyGetter

class Screen(QWidget):
    # Should be Signal(Screen) but it can't be done!
    navigation_requested = Signal(QWidget)

    def __init__(self):
        super().__init__()

    def emit_navigation(self, screen):
        self.navigation_requested.emit(screen)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monster Tamer")
        self.setFixedSize(QSize(1024, 768))
        self.setDisplayedWidget(LoginScreen())

    def setDisplayedWidget(self, screen: Screen):
        screen.navigation_requested.connect(self.setDisplayedWidget)
        # Reminder: the moment a widget drops out of the widget tree, it is destroyed
        self.setCentralWidget(screen)

class LoginScreen(Screen):

    def __init__(self):
        super().__init__()
        self.spcrs = [QSpacerItem(0,self.height()*(1/3)),QSpacerItem(0,self.height()*(1/3))]
        self.usernameLabLine = LabeledLineEdit("Username")
        self.pwdLabLine = LabeledLineEdit("Pasword")

        layout = QVBoxLayout()

        tit = QLabel("Monster Tamer", alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        fnt = QFont()
        fnt.setPointSize(50)
        fnt.setWeight(QFont.Weight.Bold)
        tit.setFont(fnt)

        loginBtn = RequestButton(StubLoginRequester(), BodyGetter(), lambda _: self.emit_navigation(MainScreen())).setTextB("Login")
        registerBtn = RequestButton(StubLoginRequester(), BodyGetter()).setTextB("Register")

        self.buttons = subWidget([loginBtn, registerBtn], ORIENTATION.HORIZONTAL)

        layout.addWidget(tit)
        layout.addSpacerItem(self.spcrs[0])
        layout.addWidget(self.usernameLabLine, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.pwdLabLine, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.buttons)
        layout.addSpacerItem(self.spcrs[1])

        self.setLayout(layout)

    def resizeEvent(self: Self, event: QResizeEvent):
        w, h = event.size().width(), event.size().height()
        self.usernameLabLine.setFixedWidth(2*w/3)
        self.pwdLabLine.setFixedWidth(2*w/3)
        for sp in self.spcrs:
            sp.changeSize(0, h/3)

    def reset(self):
        self.usernameLabLine.ledit.setText("")
        self.pwdLabLine.ledit.setText("")
        for el in self.buttons.children():
            for el2 in el.children():
                el2.reset()


class LabeledLineEdit(QWidget):
    def __init__(self: Self, lab: str) -> Self:
        super().__init__()
        lay = QHBoxLayout()
        self.label = QLabel(lab)
        self.ledit = QLineEdit()
        lay.addWidget(self.label)
        lay.addWidget(self.ledit)
        self.setLayout(lay)

class MainScreen(Screen):

    def __init__(self: Self):
        super().__init__()
        lay = QVBoxLayout()
        btn = QPushButton("Go back")
        btn.clicked.connect(lambda: self.emit_navigation(LoginScreen()))
        lay.addWidget(btn)
        self.setLayout(lay)
