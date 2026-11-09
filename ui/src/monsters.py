from PySide6.QtGui import QImage, QColor
from PySide6.QtCore import QSize
from dataclasses import dataclass

def placeholderImage(w=100,h=100):
    img = QImage(QSize(w,h),QImage.Format.Format_ARGB32_Premultiplied)
    img.fill(QColor(128,128,0))
    return img

@dataclass(frozen=True)
class Move:
    power: int
    accuracy: int
    mtype: str

@dataclass(frozen=True)
class Monster:
    monster_id: int
    instance_id: int
    name: str
    image: QImage
    moves: tuple[Move | None, Move | None, Move | None, Move | None]

    def __str__(self):
        return f"Monster{{{self.monster_id},{self.instance_id},{self.name}}}"

    def __repr__(self):
        return self.__str__()

TEST_MONSTER = Monster(0, 0, "TEST_MONSTER", placeholderImage(), (Move(50, 100, "fire"), Move(160, 40, "normal"), None, None))