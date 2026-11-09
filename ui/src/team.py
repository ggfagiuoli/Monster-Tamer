from src.monsters import Monster, TEST_MONSTER
from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class Team:
    team_id: int
    monsters: tuple[Monster | None, Monster | None, Monster | None]

    def __iter__(self):
        return iter(self.monsters)

    def __str__(self):
        return f"Team{self.monsters}"

    def __repr__(self):
        return self.__str__()

TEST_TEAM = Team(0, (TEST_MONSTER, TEST_MONSTER, TEST_MONSTER))