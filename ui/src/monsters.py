from PySide6.QtGui import QImage
from dataclasses import dataclass

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

TEST_MONSTER = Monster(0, 0, "TEST_MONSTER", QImage(), (Move(50, 100, "fire"), Move(160, 40, "normal"), None, None))