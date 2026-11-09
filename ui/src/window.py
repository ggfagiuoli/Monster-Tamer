from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QScrollArea, QFrame, QGridLayout
from PySide6.QtGui import QFont, QResizeEvent, QCursor
from PySide6.QtCore import QSize, Qt, Signal, QObject, QEvent
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from typing import Self
from src.helper import subWidget, ORIENTATION, ALIGNMENT, Stretch, whFracOf, labelFromImage, subEHWidget, BidirectionalIter
from src.request_button import RequestButton
from src.requesters import StubLoginRequester
from src.body_getters import BodyGetter
from src.team import Team, TEST_TEAM
from src.monsters import Monster, TEST_MONSTER
from functools import partial

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

        tit = QLabel("Monster Tamer", alignment=ALIGNMENT.HVCENTER.value)

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
        layout.addWidget(self.usernameLabLine, alignment=ALIGNMENT.HVCENTER.value)
        layout.addWidget(self.pwdLabLine, alignment=ALIGNMENT.HVCENTER.value)
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
        self.history_btn    = QPushButton("History")
        self.friends_btn    = QPushButton("Friends")

        teamlis = [Team(1, (TEST_MONSTER, None, None)),Team(2, (None, TEST_MONSTER, None)),Team(3, (None, None, TEST_MONSTER))]
        #teamlis.extend([TEST_TEAM]*20)

        self.logout_btn.clicked.connect(lambda _: self.emit_navigation(LoginScreen()))
        self.teams_btn.clicked.connect(lambda _: self.emit_navigation(TeamsScreen(teamlis)))

        fnt = QFont()
        fnt.setPointSize(30)

        self.encounter_btn.setFont(fnt)
        self.history_btn.setFont(fnt)
        self.collection_btn.setFont(fnt)
        self.teams_btn.setFont(fnt)

        lay.addWidget(subWidget([self.logout_btn, Stretch(1), self.friends_btn], ORIENTATION.HORIZONTAL))
        lay.addWidget(subWidget([self.encounter_btn, self.history_btn], ORIENTATION.HORIZONTAL), alignment=ALIGNMENT.HVCENTER.value)
        lay.addWidget(subWidget([self.collection_btn, self.teams_btn], ORIENTATION.HORIZONTAL), alignment=ALIGNMENT.HVCENTER.value)
        
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

class CompactMonsterDisplay(QWidget):
    def __init__(self, monster: Monster | None):
        super().__init__()
        lay = QVBoxLayout()
        if monster is None:
            lay.addWidget(QLabel("None"), alignment=ALIGNMENT.HVCENTER.value)
        else:
            lay.addWidget(labelFromImage(monster.image), alignment=ALIGNMENT.HVCENTER.value)
            lay.addWidget(QLabel(monster.name), alignment=ALIGNMENT.HVCENTER.value)
        self.setLayout(lay)

class TeamDisplay(QFrame):
    clicked = Signal(object)

    def __init__(self: Self, team: Team):
        super().__init__()
        self.team = team
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        lay = QHBoxLayout()
        for monster in team:
            lay.addWidget(CompactMonsterDisplay(monster))
        self.setLayout(lay)
        self.setObjectName("TeamDisplay")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.team)
        super().mousePressEvent(event)

    def setHovered(self, b: bool):
        if b:
            self.setStyleSheet("QFrame#TeamDisplay { border: 2px solid #880000; border-radius: 5px }")
        else:
            self.setStyleSheet("")


    def enterEvent(self, _):
        self.setHovered(True)

    def leaveEvent(self, _):
        self.setHovered(False)
        

class TeamsScreen(Screen):
    def __init__(self: Self, teams: list[Team]):
        super().__init__()
        lay = QVBoxLayout()

        self.back_btn    = QPushButton("<- Back")
        ts = [TeamDisplay(team) for team in teams]
        for t in ts:
            t.clicked.connect(partial(self.team_display_click, t.team))
        self.team_displays = subEHWidget(ts, ORIENTATION.VERTICAL)
        self.scroll_area = QScrollArea()

        self.back_btn.clicked.connect(lambda _: self.emit_navigation(MainScreen()))

        self.scroll_area.setWidget(self.team_displays)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.update_hover)

        lay.addWidget(subWidget([self.back_btn, Stretch(9)], ORIENTATION.HORIZONTAL))
        lay.addWidget(self.scroll_area)

        self.setLayout(lay)

    def update_hover(self):
        pos = self.scroll_area.viewport().mapFromGlobal(QCursor.pos())
        wid = self.scroll_area.viewport().childAt(pos)
        for td in self.team_displays.findChildren(TeamDisplay):
            td.setHovered(False)
        while wid is not None:
            if isinstance(wid, TeamDisplay):
                wid.setHovered(True)
                break
            wid = wid.parent()

    def team_display_click(self, team, _):
        self.emit_navigation(MonsterInfoScreen(BidirectionalIter(team, 0)))

class MonsterInfoPanel(Screen):
    def __init__(self, monster: Monster | None):
        super().__init__()
        lay = QGridLayout()
        if monster is None:
            lay.addWidget(QLabel("None"), 0, 0)
        else:
            lay.addWidget(subWidget([labelFromImage(monster.image), QLabel(monster.name)], ORIENTATION.VERTICAL), 0, 0, 1, 2, alignment=ALIGNMENT.HVCENTER.value)
            lay.addWidget(subWidget([QLabel(monster.name), *[QLabel(f"Stat {x}") for x in range(6)]], ORIENTATION.VERTICAL), 1, 0, alignment=ALIGNMENT.HVCENTER.value)
            lay.addWidget(subWidget([QLabel(f"Move {x}: {y}") for (x, y) in enumerate(monster.moves)], ORIENTATION.VERTICAL), 1, 1, alignment=ALIGNMENT.HVCENTER.value)
        self.setLayout(lay)

class MonsterInfoScreen(Screen):
    def __init__(self, it: BidirectionalIter):
        super().__init__()
        self.it = it
        lay = QHBoxLayout()
        btn1 = QPushButton("<")
        btn1.clicked.connect(lambda _: self.emit_navigation(MonsterInfoScreen(self.it.prev_and_self())))
        lay.addWidget(btn1, 1)
        if not it.has_prev():
            btn1.setDisabled(True)
        lay.addWidget(MonsterInfoPanel(it.current()), 8)
        btn2 = QPushButton(">")
        btn2.clicked.connect(lambda _: self.emit_navigation(MonsterInfoScreen(self.it.next_and_self())))
        lay.addWidget(btn2, 1)
        if not it.has_next():
            btn2.setDisabled(True)
        self.setLayout(lay)

