FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS req
WORKDIR /src
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --only-group worker-dbt --no-hashes --no-emit-project -o /requirements.txt

FROM python:3.12-slim
COPY --from=req /requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt


ENV DBT_SEND_ANONYMOUS_USAGE_STATS=false

COPY docker/worker/dbt/profiles.yml /etc/dbt/profiles.yml
ENV DBT_PROFILES_DIR=/etc/dbt
WORKDIR /usr/app/dbt
COPY include/dbt .
