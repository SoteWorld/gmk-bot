from __future__ import annotations

from pathlib import Path
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent


class Config(BaseSettings):
    """Настройки приложения, загруженные из переменных среды."""
    BOT_TOKEN: SecretStr
    WEBAPP_URL: str
    WEBHOOK_URL: str
    WEBHOOK_PATH: str = "/webhook"

    APP_HOST: str = "localhost"
    APP_PORT: int = 8080

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
    )


config = Config()
bot = Bot(config.BOT_TOKEN.get_secret_value())
dp = Dispatcher()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await bot.set_webhook(
        url=f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}",
        drop_pending_updates=True,
        allowed_updates=dp.resolve_used_update_types()
    )
    yield
    await bot.session.close()


app = FastAPI(lifespan=lifespan)
