from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI, Header
from pydantic import BaseModel
import time
import psutil
import logging
import uuid

historico_sessoes = {}

class ChatRequest(BaseModel):
    mensagem: str

class ChatResponse(BaseModel):
   resposta: str
   chat_id: str

class HistoryResponse(BaseModel):
    chat_id: str
    messages: list[str]

template = """
CONTEXT:
{contexto}

USER: {mensagem}
IA:
"""

llm = OllamaLLM(model="llama3.2:1b", temperature=0.4)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm

def obter_resposta(contexto: str, mensagem_usuario: str) -> str:
    resposta = chain.invoke({"contexto": contexto, "mensagem": mensagem_usuario})
    return resposta

app = FastAPI(
    title = "API ChatBot"
)

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, chat_id: str = Header(None)):

    if chat_id is None:
        chat_id = str(uuid.uuid4())
        historico_sessoes[chat_id] = []
    else:
        if chat_id not in historico_sessoes:
            historico_sessoes[chat_id] = []


    start = time.time()

    mensagem = request.mensagem
    historico = historico_sessoes[chat_id]
    contexto = "\n".join(historico[-10:])

    resposta = obter_resposta(contexto, mensagem)

    historico.append(f"USER: {mensagem}")
    historico.append(f"IA: {resposta}")

    duration = time.time() - start
    milis = int((duration % 1) * 1000)
    duration_formated = time.strftime("%H:%M:%S", time.gmtime(duration))
    print(f"Requisicao processada em {duration_formated}.{milis:03d}")
    
    return {"resposta":resposta,"chat_id":chat_id}

@app.get("/chat/{chat_id}", response_model=HistoryResponse)
def get_chat_history(chat_id: str):  
    return {"chat_id": chat_id, "messages": historico_sessoes[chat_id]}