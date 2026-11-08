from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QSpacerItem, QPushButton
from PySide6.QtGui import QFont, QResizeEvent
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from typing import Self
from src.helper import subWidget, ORIENTATION, Stretch, whFracOf
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
        self.network_mgt = QNetworkAccessManager()

    def setDisplayedWidget(self, screen: Screen):
        screen.navigation_requested.connect(self.setDisplayedWidget)
        # Reminder: the moment a widget drops out of the widget tree, it is destroyed
        self.setCentralWidget(screen)

class LoginScreen(Screen):

    def __init__(self):
        super().__init__()
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

        layout.addStretch(1)
        layout.addWidget(tit)
        layout.addStretch(1)
        layout.addWidget(self.usernameLabLine, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.pwdLabLine, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.buttons)
        layout.addStretch(1)

        self.setLayout(layout)

    def resizeEvent(self: Self, event: QResizeEvent):
        whFracOf([(self.usernameLabLine, 2/3, None), (self.pwdLabLine, 2/3, None)], event.size())



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

        self.logout_btn     = QPushButton("Log Out")
        self.encounter_btn  = QPushButton("Encounters")
        self.collection_btn = QPushButton("Collection")
        self.teams_btn      = QPushButton("Teams")
        self.history_btn = QPushButton("History")
        self.friends_btn = QPushButton("Friends")

        self.logout_btn.clicked.connect(lambda _: self.navigation_requested.emit(LoginScreen()))

        fnt = QFont()
        fnt.setPointSize(30)

        self.encounter_btn.setFont(fnt)
        self.history_btn.setFont(fnt)
        self.collection_btn.setFont(fnt)
        self.teams_btn.setFont(fnt)

        lay.addWidget(subWidget([self.logout_btn, Stretch(8), self.friends_btn], ORIENTATION.HORIZONTAL))
        lay.addWidget(subWidget([self.encounter_btn, self.history_btn], ORIENTATION.HORIZONTAL), alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        lay.addWidget(subWidget([self.collection_btn, self.teams_btn], ORIENTATION.HORIZONTAL), alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
        self.setLayout(lay)

    def resizeEvent(self: Self, event: QResizeEvent):
        whFracOf(
            [
                (self.encounter_btn, 0.4, 0.4),
                (self.collection_btn, 0.4, 0.4),
                (self.teams_btn, 0.4, 0.4),
                (self.history_btn, 0.4, 0.4)
            ],
            event.size()
        )
