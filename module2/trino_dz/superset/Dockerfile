FROM apache/superset:4.1.2

USER root

RUN python -m pip install --no-cache-dir \
    psycopg2-binary \
    sqlalchemy-trino \
    trino

USER superset
