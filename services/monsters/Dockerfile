FROM python:3.15.2-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# A user without root rights. The requirements say every container runs in user mode.
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y pip setuptools \
    && rm -rf /usr/local/lib/python3.15/ensurepip

COPY app ./app

USER app

EXPOSE 5002

# HTTPS directly in the service, using the certificate mounted by docker compose.
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", "--port", "5002", \
     "--ssl-keyfile", "/certs/service.key", \
     "--ssl-certfile", "/certs/service.crt"]
