from src.monsters import Monster, TEST_MONSTER
from dataclasses import dataclass

@dataclass(frozen=True)
class Team:
    monsters: tuple[Monster | None, Monster | None, Monster | None]

TEST_TEAM = Team((TEST_MONSTER, TEST_MONSTER, TEST_MONSTER))