from pathlib import Path
from pydantic_settings import BaseSettings


PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]


class AppConfig(BaseSettings):
    BOT_TOKEN: str
    PAYMENTS_TOKEN: str

    PG_DB: str
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int

    @property
    def DB_URI(self):
        return (
            f"postgresql://{self.PG_USER}:{self.PG_PASSWORD}@"
            f"{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
        )

    class Config:
        extra = "ignore"
        env_file = PROJECT_ROOT / ".env"


APP_CONF = AppConfig()
