import os

c = get_config()

hub_dir = os.environ.get("JUPYTERHUB_DATA_DIR", "/srv/jupyterhub-data")
work_dir = os.environ.get("JUPYTER_WORK_DIR", "/home/jovyan/work")
admin_name = os.environ.get("JUPYTERHUB_ADMIN_USER", "admin")

notebook_env = {
    key: os.environ.get(key, default)
    for key, default in {
        "POSTGRES_HOST": "postgres",
        "POSTGRES_PORT": "5432",
        "POSTGRES_DB": "oil_analytics",
        "POSTGRES_USER": "admin",
        "POSTGRES_PASSWORD": "admin",
        "MINIO_ENDPOINT": "http://minio:9000",
        "MINIO_ACCESS_KEY": "admin",
        "MINIO_SECRET_KEY": "adminadmin",
        "MINIO_BUCKET": "oil-lake",
    }.items()
}


c.JupyterHub.bind_url = "http://0.0.0.0:8000"
c.JupyterHub.default_url = "/hub/spawn"
c.JupyterHub.db_url = f"sqlite:///{hub_dir}/jupyterhub.sqlite"
c.JupyterHub.cookie_secret_file = f"{hub_dir}/jupyterhub_cookie_secret"

c.JupyterHub.authenticator_class = "jupyterhub.auth.DummyAuthenticator"
c.JupyterHub.spawner_class = "jupyterhub.spawner.SimpleLocalProcessSpawner"
c.Authenticator.allow_all = True
c.Authenticator.allowed_users = {admin_name}
c.DummyAuthenticator.password = os.environ.get("JUPYTERHUB_ADMIN_PASSWORD", "admin")
c.ConfigurableHTTPProxy.check_running_interval = 15

c.Spawner.default_url = "/lab"
c.Spawner.notebook_dir = work_dir
c.Spawner.start_timeout = 120
c.Spawner.http_timeout = 120
c.Spawner.environment = notebook_env
