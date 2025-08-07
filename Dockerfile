FROM python:3.10-slim AS base

WORKDIR /app

FROM base AS builder

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --no-dev

COPY /app ./app
COPY main.py .

EXPOSE 8000
