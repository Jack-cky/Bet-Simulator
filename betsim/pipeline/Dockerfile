FROM python:3.12.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    UV_SYSTEM_PYTHON=1 \
    UV_NO_CACHE=1

WORKDIR /app

COPY config/config.toml ./config/config.toml
COPY betsim/shared ./betsim/shared
COPY betsim/pipeline ./betsim/pipeline
COPY pyproject.toml ./

RUN --mount=from=ghcr.io/astral-sh/uv:0.10.11,source=/uv,target=/bin/uv \
    apt-get update && \
    apt-get install -y --no-install-recommends git libgomp1 && \
    uv pip install ".[pipeline]" && \
    uv pip uninstall nvidia-nccl-cu12 kaleido && \
    apt-get purge -y --auto-remove git && \
    rm -rf /var/lib/apt/lists/* && \
    useradd --create-home betsim && \
    chown -R betsim:betsim /app

USER betsim

CMD ["python", "-m", "betsim.pipeline.main"]
