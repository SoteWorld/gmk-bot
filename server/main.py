from __future__ import annotations

import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from server.config_reader import config, app, dp
from server.bot.handlers import setup_routers as setup_bot_routers
from server.routes import setup_routers as setup_http_routers

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dp.include_router(setup_bot_routers())
app.include_router(setup_http_routers())

if __name__ == "__main__":
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)
