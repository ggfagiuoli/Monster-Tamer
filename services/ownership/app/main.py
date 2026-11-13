"""Ownership service: which monsters each player owns, and their teams.

The API it should end up with is docs/ownership.yaml.
"""

from fastapi import FastAPI

app = FastAPI(title="Monster Tamers - Ownership", version="0.1.0")


@app.get("/health")
def health() -> dict:
    """Used by docker compose to know the service is up."""
    return {"status": "ok"}


@app.get("/collection", status_code=501)
def placeholder() -> dict:
    # TODO: implement from docs/ownership.yaml
    return {"error": "not_implemented", "message": "Coming soon."}
