#!/usr/bin/env bash

set -euo pipefail
docker run --rm --network airflow-template_default \
  -e POLARIS_PERSISTENCE_TYPE=relational-jdbc \
  -e POLARIS_PERSISTENCE_RELATIONAL_JDBC_DATABASE_TYPE=postgresql \
  -e QUARKUS_DATASOURCE_JDBC_URL='jdbc:postgresql://postgres:5432/airflow?currentSchema=polaris' \
  -e QUARKUS_DATASOURCE_USERNAME=airflow \
  -e QUARKUS_DATASOURCE_PASSWORD=airflow \
  "apache/polaris-admin-tool:${POLARIS_VERSION:-1.8.0}" \
  bootstrap --realm=POLARIS --credential=POLARIS,root,s3cr3t
