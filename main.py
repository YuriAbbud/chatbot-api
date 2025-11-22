from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI, Header
from pydantic import BaseModel
from collections import OrderedDict
import time
import logging
import uuid

hoje = time.strftime("%F")
logging.basicConfig(
    level=logging.INFO,
    filename=f"{hoje}.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

historico_sessoes = {}
cache_local = OrderedDict()
cache_max_size = 100

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
    try:

        if chat_id is None:
            chat_id = str(uuid.uuid4())
            historico_sessoes[chat_id] = []

            logging.info(f"Novo chat_id criado: {chat_id}")

        else:
            if chat_id not in historico_sessoes:
                historico_sessoes[chat_id] = []

        start = time.time()

        mensagem = request.mensagem
        historico = historico_sessoes[chat_id]
        contexto = "\n".join(historico[-10:])

        logging.info(f"Mensagem recebida do usuário ({chat_id}): {mensagem}")


        if mensagem in cache_local:
            cache_local.move_to_end(mensagem)
            resposta = cache_local[mensagem]
        else:
            if len(cache_local) > cache_max_size:
                logging.warning(f"Cache local alcançando limite máximo: {len(cache_local)}/{cache_max_size}")
                cache_local.popitem(last=False)
            
            try:
                resposta = obter_resposta(contexto, mensagem)
            except Exception as e:
                logging.error(f"Erro ao obter resposta do modelo para mensagem = {mensagem}, contexto = {contexto}, chat_id {chat_id}: {e}")
                resposta("Houve um erro na geração da resposta! Por favor, tente novamente.")

            cache_local[mensagem] = resposta

        historico.append(f"USER: {mensagem}")
        historico.append(f"IA: {resposta}")

        if len(historico) > 200:
            logging.warning(f"Histórico do chat {chat_id} excedeu 200 mensagens. Pode impactar memória.") 

        duration = time.time() - start
        milis = int((duration % 1) * 1000)
        duration_formated = time.strftime("%H:%M:%S", time.gmtime(duration))
        
        logging.info(f"Tempo de processamento da requisição: {duration_formated}.{milis:03d}")
        
        return {"resposta":resposta,"chat_id":chat_id}
    
    except Exception as e:
        logging.critical(f"Erro crítico: {e}")
        return {"resposta": "Erro interno no servidor", "chat_id": chat_id or "indefinido"}

@app.get("/chat/{chat_id}", response_model=HistoryResponse)
def get_chat_history(chat_id: str):
    try:
        if chat_id not in historico_sessoes:
            logging.error(f"Tentativa de acessar histórico inexistente: {chat_id}")
            return {"chat_id": chat_id, "messages": f"Não foi encontrado um histórico para o chat_id = {chat_id}"}
        else:
            return {"chat_id": chat_id, "messages": historico_sessoes[chat_id]}
    except Exception as e:
        logging.error(f"Erro ao buscar histórico, chat_id = {chat_id}: {e}")
        return {"chat_id": chat_id, "messages": f"Houve um erro ao buscar histórico do chat_id = {chat_id}: {e}"}