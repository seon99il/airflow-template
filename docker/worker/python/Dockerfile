FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS req
WORKDIR /src
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --only-group worker-python --no-hashes --no-emit-project -o /requirements.txt

FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=req /requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY include/python-worker /app/python-worker
ENV PYTHONPATH=/app/python-worker
WORKDIR /app
