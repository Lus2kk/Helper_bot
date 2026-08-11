from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    gnews_api_url: str
    gnews_api_key: SecretStr
    open_meteo_api_url: str
    
    tg_bot_token: SecretStr
    
    db_host: str
    db_port: int
    db_user: str
    db_password: SecretStr
    db_name: str
   
    app_port: int
    webhook_url: str = ""

    @property
    def database_url_async(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password.get_secret_value()}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def database_url_sync(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password.get_secret_value()}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=False,
        extra="ignore",
        
    )

settings = Settings()  

