#!/usr/bin/env bash

set -euo pipefail
POLARIS=http://localhost:8181

code=$(curl -s -o /dev/null -w '%{http_code}' -X PUT --aws-sigv4 'aws:amz:us-east-1:s3' -u rustfs:rustfs123 http://localhost:9000/warehouse)
case $code in 200|409) echo "bucket ok ($code)";; *) echo "bucket failed ($code)"; exit 1;; esac

TOKEN=$(curl -sf $POLARIS/api/catalog/v1/oauth/tokens \
  -d grant_type=client_credentials -d client_id=root -d client_secret=s3cr3t -d scope=PRINCIPAL_ROLE:ALL \
  | sed -n 's/.*"access_token":"\([^"]*\)".*/\1/p')

out=$(mktemp)
code=$(curl -s -o "$out" -w '%{http_code}' $POLARIS/api/management/v1/catalogs \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"catalog": {"name": "default", "type": "INTERNAL", "properties": {"default-base-location": "s3://warehouse"},
       "storageConfigInfo": {"storageType": "S3", "allowedLocations": ["s3://warehouse"], "region": "us-east-1",
                             "endpoint": "http://rustfs:9000", "pathStyleAccess": true}}}')
case $code in 201|409) echo "catalog ok ($code)";; *) cat "$out"; exit 1;; esac

curl -sf -X PUT $POLARIS/api/management/v1/catalogs/default/catalog-roles/catalog_admin/grants \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"type": "catalog", "privilege": "CATALOG_MANAGE_CONTENT"}' && echo "grant ok"
