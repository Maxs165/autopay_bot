import logging
from pathlib import Path
from pydantic_settings import BaseSettings
from colorama import Fore


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


class LoggingConfig(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = PROJECT_ROOT / "logs.log"
    LOG_FORMAT: str = (
        "[%(asctime)s]:" "[%(levelname)-8s]:" "[%(name)s]:" "[%(filename)s]:::" "%(message)s"
    )
    LOG_FORMAT_COLORS: str = (
        Fore.BLUE
        + "[%(asctime)s]:"
        + Fore.CYAN
        + "[%(levelname)-8s]:"
        + Fore.GREEN
        + "[%(name)s]:"
        + Fore.MAGENTA
        + "[%(filename)s]:::"
        + Fore.WHITE
        + "%(message)s"
    )

    class Config:
        extra = "ignore"
        env_file = PROJECT_ROOT / ".env"


def configure_logger():
    basic_formatter = logging.Formatter(LOG_CONF.LOG_FORMAT)
    colored_formatter = logging.Formatter(LOG_CONF.LOG_FORMAT_COLORS)
    # json_formatter = jsonlogger.JsonFormatter()

    file_handler = logging.FileHandler(LOG_CONF.LOG_FILE)
    file_handler.setFormatter(basic_formatter)
    # file_handler.setFormatter(json_formatter)

    std_handler = logging.StreamHandler()
    std_handler.setFormatter(colored_formatter)

    logger = logging.getLogger()
    logger.setLevel(LOG_CONF.LOG_LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(std_handler)


LOG_CONF = LoggingConfig()

configure_logger()

APP_CONF = AppConfig()
