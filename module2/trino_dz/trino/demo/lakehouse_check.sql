CREATE SCHEMA IF NOT EXISTS hive.oil;

DROP TABLE IF EXISTS hive.oil.production_parquet;

CREATE TABLE hive.oil.production_parquet (
    prod_id integer,
    well_id integer,
    date date,
    oil_ton double,
    gas_m3 double,
    water_m3 double,
    energy_kwh double,
    downtime_hours double,
    temperature double,
    pressure double,
    dt date
)
WITH (
    external_location = 's3://oil-lake/bronze/production',
    format = 'PARQUET',
    partitioned_by = ARRAY['dt']
);

CALL hive.system.sync_partition_metadata('oil', 'production_parquet', 'FULL');

SELECT dt, count(*) AS rows_count, round(sum(oil_ton), 2) AS oil_ton
FROM hive.oil.production_parquet
GROUP BY dt
ORDER BY dt
LIMIT 10;
