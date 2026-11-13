FROM python:3.15.2-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# A user without root rights. The requirements say every container runs in user mode.
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app

WORKDIR /app

# Install dependencies first so docker can cache this layer between builds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y pip setuptools \
    && rm -rf /usr/local/lib/python3.15/ensurepip

COPY app ./app

# Everything after this line runs as the non-root user.
USER app

# Encounter service listens on port 5003.
EXPOSE 5003

# HTTPS directly in the service, using the certificate mounted by docker compose.
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", "--port", "5003", \
     "--ssl-keyfile", "/certs/service.key", \
     "--ssl-certfile", "/certs/service.crt"]
