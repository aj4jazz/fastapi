from pydantic.v1 import BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    #model_config = SettingsConfigDict(validate_default=False)

    database_hostname: str = Field('', validate_default=False)
    database_port: str = Field('', validate_default=False)
    database_password: str = Field('', validate_default=False)
    database_name: str = Field('', validate_default=False)
    database_username: str = Field('', validate_default=False)
    secret_key: str = Field('', validate_default=False)
    algorithm: str = Field('', validate_default=False)
    access_token_expire_minutes: int = Field(1, validate_default=False)

    class Config:
        env_file = ".env"


settings = Settings()