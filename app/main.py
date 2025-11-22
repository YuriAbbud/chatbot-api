from fastapi import FastAPI
from app.api.routes.chat_routes import router
from app.core.logger import setup_logging
from app.core.config import LOG_FILENAME

setup_logging(LOG_FILENAME)

app = FastAPI(title="API ChatBot")
app.include_router(router, prefix="/chat")