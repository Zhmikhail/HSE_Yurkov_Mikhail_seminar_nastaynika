FROM quay.io/jupyter/base-notebook:python-3.12

USER root

ENV NOTEBOOK_HUB_CONFIG=/srv/jupyterhub/notebook_server_config.py

RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs npm \
    && npm install -g configurable-http-proxy \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir \
    boto3 \
    joblib \
    jupyterhub==5.2.1 \
    jupyterlab \
    matplotlib \
    pandas \
    psycopg2-binary \
    pyarrow \
    s3fs \
    scikit-learn \
    seaborn \
    sqlalchemy \
    sqlalchemy-trino \
    trino

RUN mkdir -p /srv/jupyterhub-data \
    && chown -R jovyan:users /srv/jupyterhub-data

COPY notebook_server_config.py ${NOTEBOOK_HUB_CONFIG}

USER jovyan
WORKDIR /home/jovyan/work

CMD ["sh", "-c", "jupyterhub -f ${NOTEBOOK_HUB_CONFIG}"]
