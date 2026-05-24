from __future__ import annotations

from dataclasses import dataclass

import boto3
import pandas as pd
from sqlalchemy import create_engine, text

from project_env import MINIO, postgres_url, s3_storage_options


@dataclass(frozen=True)
class ExportJob:
    table: str
    partition_source: str | None = None


EXPORT_JOBS = (
    ExportJob("wells"),
    ExportJob("production", "date"),
    ExportJob("well_telemetry", "timestamp"),
    ExportJob("well_targets", "date"),
    ExportJob("pumps"),
    ExportJob("pump_sensors", "timestamp"),
    ExportJob("pump_failures", "failure_date"),
    ExportJob("deliveries", "date"),
    ExportJob("drivers"),
    ExportJob("vehicles"),
    ExportJob("oil_stations"),
)


def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=MINIO["endpoint_url"],
        aws_access_key_id=MINIO["aws_access_key_id"],
        aws_secret_access_key=MINIO["aws_secret_access_key"],
    )


def prepare_bucket() -> None:
    client = s3_client()
    buckets = {bucket["Name"] for bucket in client.list_buckets()["Buckets"]}
    if MINIO["bucket"] not in buckets:
        client.create_bucket(Bucket=MINIO["bucket"])


def normalize_dates(frame: pd.DataFrame) -> pd.DataFrame:
    prepared = frame.copy()
    date_like = [
        column
        for column in prepared.columns
        if column.endswith("_date") or column in {"date", "install_date", "failure_date", "timestamp"}
    ]
    for column in date_like:
        prepared[column] = pd.to_datetime(prepared[column])
    return prepared


def fill_numeric_gaps(frame: pd.DataFrame) -> pd.DataFrame:
    numeric_columns = frame.select_dtypes(include="number").columns
    if len(numeric_columns) == 0:
        return frame
    result = frame.copy()
    result[numeric_columns] = result[numeric_columns].fillna(result[numeric_columns].median(numeric_only=True))
    return result


def add_partition(frame: pd.DataFrame, source_column: str | None) -> pd.DataFrame:
    result = normalize_dates(frame)
    result = fill_numeric_gaps(result)
    if source_column is None:
        result["dt"] = pd.Timestamp("2025-10-01").date()
    else:
        result["dt"] = result[source_column].dt.date
    return result


def read_table(engine, table_name: str) -> pd.DataFrame:
    query = text(f"SELECT * FROM {table_name}")
    return pd.read_sql(query, engine)


def write_outputs(frame: pd.DataFrame, table_name: str) -> None:
    options = s3_storage_options()
    bucket = MINIO["bucket"]
    frame.to_parquet(
        f"s3://{bucket}/bronze/{table_name}",
        engine="pyarrow",
        partition_cols=["dt"],
        index=False,
        storage_options=options,
    )
    frame.to_csv(f"s3://{bucket}/csv/{table_name}.csv", index=False, storage_options=options)


def run_job(engine, job: ExportJob) -> int:
    raw_frame = read_table(engine, job.table)
    prepared_frame = add_partition(raw_frame, job.partition_source)
    write_outputs(prepared_frame, job.table)
    return len(prepared_frame)


def main() -> None:
    prepare_bucket()
    engine = create_engine(postgres_url())
    for job in EXPORT_JOBS:
        row_count = run_job(engine, job)
        print(f"exported {job.table}: {row_count} rows")


if __name__ == "__main__":
    main()
