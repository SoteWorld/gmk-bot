from aiogram.types import Update
from fastapi import APIRouter, Request

from server.config_reader import config, bot, dp

router = APIRouter()

@router.post(config.WEBHOOK_PATH)
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
