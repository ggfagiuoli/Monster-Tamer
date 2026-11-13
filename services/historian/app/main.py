"""Historian service: the record of every finished run.

The API it should end up with is docs/historian.yaml.
"""

from fastapi import FastAPI

app = FastAPI(title="Monster Tamers - Historian", version="0.1.0")


@app.get("/health")
def health() -> dict:
    """Used by docker compose to know the service is up."""
    return {"status": "ok"}


@app.get("/history", status_code=501)
def placeholder() -> dict:
    # TODO: implement from docs/historian.yaml
    return {"error": "not_implemented", "message": "Coming soon."}
