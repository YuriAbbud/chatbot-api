import logging
from fastapi import APIRouter, HTTPException, Header
from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse
from app.services.chat_service import ChatService
from app.services.history_service import get_history

router = APIRouter()
service = ChatService()

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, chat_id: str = Header(None)):
    try:
        resposta = service.process_message(request.mensagem, chat_id)
        return ChatResponse(resposta=resposta, chat_id=chat_id)
    except Exception as e:
        logging.critical(f"Erro inesperado no endpoint: {e}")
        raise HTTPException(500, "Erro interno no servidor")

@router.get("/{chat_id}")
def history(chat_id: str):
    return {"chat_id": chat_id, "messages": get_history(chat_id)}