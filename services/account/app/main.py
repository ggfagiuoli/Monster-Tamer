"""Account service: player registration, login and profile.

The API it should end up with is docs/openapi/account.yaml.
"""

from fastapi import FastAPI

app = FastAPI(title="Monster Tamers - Account", version="0.1.0")


@app.get("/health")
def health() -> dict:
    """Used by docker compose to know the service is up."""
    return {"status": "ok"}


@app.post("/auth/register", status_code=501)
def register() -> dict:
    # TODO (task 8): implement from docs/openapi/account.yaml
    return {"error": "not_implemented", "message": "Coming soon."}
