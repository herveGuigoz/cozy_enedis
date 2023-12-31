import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_secret: str
    public_entrypoint: str
    database_url: str
    client_name: str
    software_id: str
    oidc_server_url: str
    oidc_server_url_internal: str
    oidc_client_id: str
    oidc_client_secret: str


settings = Settings()
