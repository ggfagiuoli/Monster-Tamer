from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QSize
from dataclasses import dataclass

@dataclass(frozen=True)
class Stretch:
    size: int

    def __post_init__(self):
        object.__setattr__(self, "size", max(0, self.size))

# Merely meant to be used like an enum
class ORIENTATION:
    class ENUM:
        def __init__(self, o):
            self.o = o

        def __eq__(self, other):
            return self.o == other.o

    HORIZONTAL = ENUM(0)
    VERTICAL = ENUM(1)

def subWidget(wids: list[QWidget | Stretch], orientation: ORIENTATION.ENUM):
    qw = QWidget()
    lay = QHBoxLayout() if orientation == ORIENTATION.HORIZONTAL else QVBoxLayout()
    for wid in wids:
        if type(wid) is Stretch:
            lay.addStretch(wid.size)
            continue
        lay.addWidget(wid)
    qw.setLayout(lay)
    return qw

def whFracOf(wids_frac: list[tuple[QWidget, float | None, float | None]], sz: QSize):
    w = sz.width()
    h = sz.height()
    for (wid, fracw, frach) in wids_frac:
        if fracw is not None:
            wid.setFixedWidth(int(fracw * w))
        if frach is not None:
            wid.setFixedHeight(int(frach * h))