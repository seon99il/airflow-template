import os

from pyiceberg.catalog import load_catalog


def get_catalog():
    return load_catalog(
        "default",
        type="rest",
        uri=os.environ["POLARIS_URI"],
        warehouse="default",
        credential=os.environ["POLARIS_CREDENTIAL"],
        scope="PRINCIPAL_ROLE:ALL",
        **{
            "s3.endpoint": os.environ["S3_ENDPOINT"],
            "s3.access-key-id": os.environ["S3_ACCESS_KEY"],
            "s3.secret-access-key": os.environ["S3_SECRET_KEY"],
            "s3.path-style-access": "true",
            "s3.region": "us-east-1",
        },
    )
