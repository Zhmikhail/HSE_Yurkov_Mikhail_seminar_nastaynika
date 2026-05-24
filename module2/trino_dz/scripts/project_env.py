from __future__ import annotations

import os


def postgres_url() -> str:
    user = os.getenv("POSTGRES_USER", "admin")
    password = os.getenv("POSTGRES_PASSWORD", "admin")
    host = os.getenv("POSTGRES_HOST", "postgres")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "oil_analytics")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"


MINIO = {
    "endpoint_url": os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
    "aws_access_key_id": os.getenv("MINIO_ACCESS_KEY", "admin"),
    "aws_secret_access_key": os.getenv("MINIO_SECRET_KEY", "adminadmin"),
    "bucket": os.getenv("MINIO_BUCKET", "oil-lake"),
}


def s3_storage_options() -> dict:
    return {
        "key": MINIO["aws_access_key_id"],
        "secret": MINIO["aws_secret_access_key"],
        "client_kwargs": {"endpoint_url": MINIO["endpoint_url"]},
    }
