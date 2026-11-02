#!/usr/bin/env bash

set -euo pipefail
docker compose -f compose.dev.yaml exec -T postgres psql -U airflow -d airflow -v ON_ERROR_STOP=1 \
  -c 'CREATE SCHEMA IF NOT EXISTS marquez' \
  -c 'CREATE SCHEMA IF NOT EXISTS polaris'
