from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env")
    secret_key: str
    web_host: str
    api_host: str
    db_uri: str
    mail_api_key: str
    mail_domain: str
    node_extra_ca_certs: str


settings = Settings()
