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
   session_id: str

template = """
CONTEXT:
{contexto}

USER: {mensagem}
IA:
"""

llm = OllamaLLM(model="llama3.2:1b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm

def obter_resposta(contexto: str, mensagem_usuario: str) -> str:
    resposta = chain.invoke({"contexto": contexto, "mensagem": mensagem_usuario})
    return resposta

app = FastAPI(
    title = "API ChatBot"
)

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, session_id: str = Header(None, alias="Session-id")):

    if session_id is None:
        session_id = str(uuid.uuid4())
        historico_sessoes[session_id] = []
    else:
        if session_id not in historico_sessoes:
            historico_sessoes[session_id] = []


    start = time.time()

    mensagem = request.mensagem
    historico = historico_sessoes[session_id]
    contexto = "\n".join(historico)

    resposta = obter_resposta(contexto, mensagem)

    historico.append(f"USER: {mensagem}")
    historico.append(f"IA: {resposta}")

    duration = time.time() - start
    milis = int((duration % 1) * 1000)
    duration_formated = time.strftime("%H:%M:%S", time.gmtime(duration))
    print(f"Requisicao processada em {duration_formated}.{milis:03d}")
    
    return {"resposta":resposta,"session_id":session_id}