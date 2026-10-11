FROM python:3.12.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    UV_SYSTEM_PYTHON=1 \
    UV_NO_CACHE=1

WORKDIR /app

COPY config/config.toml ./config/config.toml
COPY betsim/shared ./betsim/shared
COPY betsim/simulator ./betsim/simulator
COPY pyproject.toml ./

RUN --mount=from=ghcr.io/astral-sh/uv:0.10.11,source=/uv,target=/bin/uv \
    uv pip install ".[simulator]" && \
    useradd --create-home betsim && \
    chown -R betsim:betsim /app

USER betsim

EXPOSE 5000

CMD ["taipy", "run", "betsim/simulator/main.py"]
