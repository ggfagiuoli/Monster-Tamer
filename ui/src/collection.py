from dataclasses import dataclass
from src.monsters import Monster, TEST_MONSTER

@dataclass(frozen=True)
class MonsterCollection:
    monsters: list[Monster]

    def __iter__(self):
        return iter(self.monsters)

TEST_COLLECTION = MonsterCollection([TEST_MONSTER] * 800)