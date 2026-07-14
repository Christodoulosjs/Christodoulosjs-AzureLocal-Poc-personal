from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    subscription_id: str
    database_connection_string: str
    custom_location_id: str
    logical_network_id: str
    tenant_id: str
    poller_client_id: str
    poller_client_secret: str
    listener_api_audience:str
    application_insights_connection_string: str
    keyvault_url:str
    aws_region: str
    sqs_queue_url: str
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()