"""monsters service: the catalogue of every monster in the game.

This is the EXAMPLE service of the skeleton. Copy this folder to make the others
(see GUIDE.md step 1). The API it should end up with is docs/openapi/monsters.yaml.
"""

from fastapi import FastAPI, HTTPException, Path

app = FastAPI(title="Monster Tamers - monsters", version="0.1.0")

# TODO (task 13): load these from the database, seeded from seed/monsters.json.
# Kept in memory for now so the skeleton runs without a database.
MONSTERS = {
    "flamepup": {
        "id": "flamepup",
        "name": "Flamepup",
        "description": "A small fire dog. Fast, but fragile.",
        "image_url": "/monsters/flamepup/image",
        "element": "fire",
        "rarity": "common",
        "starter": True,
        "stats": {"hp": 40, "attack": 55, "defense": 30, "speed": 70},
    },
    "tidefin": {
        "id": "tidefin",
        "name": "Tidefin",
        "description": "A river fish with a hard shell.",
        "image_url": "/monsters/tidefin/image",
        "element": "water",
        "rarity": "rare",
        "starter": False,
        "stats": {"hp": 60, "attack": 40, "defense": 65, "speed": 35},
    },
}


@app.get("/health")
def health() -> dict:
    """Used by docker compose to know the service is up."""
    return {"status": "ok"}


@app.get("/monsters")
def list_monsters() -> list[dict]:
    # TODO (task 8/15): require a valid player token (Authorization: Bearer ...).
    return [
        {k: m[k] for k in ("id", "name", "image_url", "element", "rarity")}
        for m in MONSTERS.values()
    ]


@app.get("/monsters/{monster_id}")
def get_monster(
    monster_id: str = Path(pattern=r"^[a-z0-9-]{1,40}$"),
) -> dict:
    monster = MONSTERS.get(monster_id)
    if monster is None:
        raise HTTPException(status_code=404, detail="This monster does not exist.")
    return monster
