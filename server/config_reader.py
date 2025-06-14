from pathlib import Path
from typing import AsyncGenerator
from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from contextlib import asynccontextmanager

ROOT_DIR = Path(__file__).parent.parent


class Config(BaseSettings):
    BOT_TOKEN: SecretStr = "8050321300:AAHMjnM7EsGq8rm3FQtRhzP2JIShGqQDvEE"

    WEBAPP_URL: str = "https://fc5a1bad75703ee866f945fa91f0f437.serveo.net"

    WEBHOOK_URL: str = "https://8486a2fc3389e779cc5dffb2fdf15839.serveo.net"
    WEBHOOK_PATH: str = "/webhook"

    APP_HOST: str = "localhost"
    APP_PORT: int = 8080

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / "server" / ".env",
        env_file_encoding="utf-8",
    )

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await bot.set_webhook(
        url=f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}",
        drop_pending_updates=True,
        allowed_updates=dp.resolve_used_update_types()
    )
    yield
    await bot.session.close()

config = Config()
bot = Bot(config.BOT_TOKEN.get_secret_value())
dp = Dispatcher()
app = FastAPI(lifespan=lifespan)

