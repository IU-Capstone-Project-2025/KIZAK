from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str

    model_config = SettingsConfigDict(env_file=[".env", ".env.example"],
                                      extra="ignore")


Config = Settings()
