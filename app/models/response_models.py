from pydantic import BaseModel

class ChatResponse(BaseModel):
    resposta: str
    chat_id: str