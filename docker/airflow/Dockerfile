FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS req
WORKDIR /src
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --only-group airflow --no-hashes --no-emit-project -o /requirements.txt

FROM apache/airflow:3.1.2-python3.12
COPY --from=req /requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
