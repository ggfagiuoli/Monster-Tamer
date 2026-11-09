from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QImage, QPixmap
from dataclasses import dataclass
from typing import Any
from enum import Enum

@dataclass(frozen=True)
class Stretch:
    size: int

    def __post_init__(self):
        object.__setattr__(self, "size", max(0, self.size))

class ORIENTATION(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class ALIGNMENT(Enum):
    HVCENTER = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter

def subWidget(wids: list[QWidget | tuple[QWidget, Stretch] | Stretch], orientation: ORIENTATION):
    qw = QWidget()
    lay = QHBoxLayout() if orientation == ORIENTATION.HORIZONTAL else QVBoxLayout()
    for wid in wids:
        if type(wid) is Stretch:
            lay.addStretch(wid.size)
            continue
        if isinstance(wid, tuple):
            (w, s) = wid
            lay.addWidget(w, s.size)
            continue
        lay.addWidget(wid)
    qw.setLayout(lay)
    return qw

def subEHWidget(wids: list[QWidget | tuple[QWidget, Stretch] | Stretch], orientation: ORIENTATION):
    return bPolicy(subWidget(wids, orientation), QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

def bPolicy(wid: QWidget, polh, polv):
    wid.setSizePolicy(polh, polv)
    return wid

def whFracOf(wids_frac: list[tuple[QWidget, float | None, float | None]], sz: QSize):
    w = sz.width()
    h = sz.height()
    for (wid, fracw, frach) in wids_frac:
        if fracw is not None:
            wid.setFixedWidth(int(fracw * w))
        if frach is not None:
            wid.setFixedHeight(int(frach * h))

def labelFromImage(img: QImage):
    lab = QLabel()
    lab.setPixmap(QPixmap.fromImage(img))
    return lab

def hExp(wid: QWidget):
    wid.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    return wid

class BidirectionalIter:
    def __init__(self, collection, start: int = -1):
        self.collection = list(collection)
        self.index = start

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def has_next(self):
        return self.index + 1 < len(self.collection)

    def has_prev(self):
        return self.index - 1 >= 0

    def next(self):
        if not self.has_next():
            raise StopIteration
        self.index += 1
        return self.collection[self.index]

    def next_and_self(self):
        self.next()
        return self

    def current(self):
        if 0 <= self.index < len(self.collection):
            return self.collection[self.index]
        print(None)
        return None

    def prev(self):
        if not self.has_prev():
            raise StopIteration
        self.index -= 1
        return self.collection[self.index]

    def prev_and_self(self):
        self.prev()
        return self
