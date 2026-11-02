import os

import polars as pl
from common.catalog import get_catalog

TABLE = "sample.numbers"


def write():
    catalog = get_catalog()
    catalog.create_namespace_if_not_exists("sample")
    df = pl.DataFrame({"n": range(1, 6)}).with_columns(squared=pl.col("n") ** 2)
    table = catalog.create_table_if_not_exists(TABLE, schema=df.to_arrow().schema)
    df.write_iceberg(table, mode="overwrite")
    print(f"wrote {df.height} rows to {TABLE}")


def read():
    storage_options = {
        "aws_endpoint_url": os.environ["S3_ENDPOINT"],
        "aws_access_key_id": os.environ["S3_ACCESS_KEY"],
        "aws_secret_access_key": os.environ["S3_SECRET_KEY"],
        "aws_region": "us-east-1",
        "aws_allow_http": "true",
    }
    table = get_catalog().load_table(TABLE)
    print(pl.scan_iceberg(table, storage_options=storage_options).collect())
