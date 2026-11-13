"""Encounter service: encounters and the runs players make through them.

The API it should end up with is docs/encounter.yaml.
"""

from fastapi import FastAPI

app = FastAPI(title="Monster Tamers - Encounter", version="0.1.0")


@app.get("/health")
def health() -> dict:
    """Used by docker compose to know the service is up."""
    return {"status": "ok"}


@app.get("/encounters", status_code=501)
def placeholder() -> dict:
    # TODO: implement from docs/encounter.yaml
    return {"error": "not_implemented", "message": "Coming soon."}
