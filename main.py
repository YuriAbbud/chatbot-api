from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from fastapi import FastAPI
from pydantic import BaseModel
import time
import psutil
import logging

class ChatRequest(BaseModel):
    mensagem: str

class ChatResponse(BaseModel):
    resposta: str

llm = OllamaLLM(model="llama3.2:1b")
prompt = PromptTemplate.from_template("{mensagem}")
chain = prompt | llm

def obter_resposta(mensagem_usuario: str) -> str:
    resposta = chain.invoke({"mensagem": mensagem_usuario})
    return resposta

app = FastAPI(
    title = "API ChatBot"
)

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    start = time.time()

    mensagem = request.mensagem

    resposta = obter_resposta(mensagem)

    duration = time.time() - start
    duration_formated = time.strftime("%H:%M:%S", time.gmtime(duration))
    print(f"Requisicao processada em {duration_formated} segundos.")
    
    return {"resposta":resposta}

@app.get("/metrics")
def get_metrics():
    return {
        "cpu_usage": f"{psutil.cpu_percent()}%",
        "memory_usage": f"{psutil.virtual_memory().percent}%"
    }

