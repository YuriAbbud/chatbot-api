import logging
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from app.core.config import LLM_MODEL_NAME, CACHE_MAX_SIZE
from app.services.cache_service import LocalCache
from app.services.history_service import get_history, append_history

template = """
CONTEXT:
{contexto}

USER: {mensagem}
IA:
"""

class ChatService:
    def __init__(self):
        self.cache = LocalCache(CACHE_MAX_SIZE)
        self.llm = OllamaLLM(model=LLM_MODEL_NAME, temperature=0.4)
        self.prompt = ChatPromptTemplate.from_template(template)

    def process_message(self, mensagem: str, chat_id: str):

        if not mensagem or mensagem.strip() == "":
            logging.error(f"[{chat_id}] Mensagem vazia recebida.")
            return "A mensagem enviada está vazia. Por favor, envie um texto válido."
        
        historico = get_history(chat_id)
        contexto = "\n".join(historico[-20:])

        cached = self.cache.get(mensagem)
        if cached:
            logging.info(f"[{chat_id}] Cache contem resposta para mensagem: {mensagem}")
            resposta = cached
        else:
            logging.info(f"[{chat_id}] Cache não contem resposta para mensagem: {mensagem}")
            prompt_final = f"""
            CONTEXT:
            {contexto}

            USER: {mensagem}
            IA:
            """.strip()

            try:
                resposta = self.llm.invoke(prompt_final)
            except Exception as e:
                logging.error(f"[{chat_id}] Erro ao chamar o modelo: {e}")
                return "Desculpe, ocorreu um erro ao processar sua solicitação"


            logging.info(f"[{chat_id}] Resposta gerada e adicionada ao cache.")
            self.cache.set(mensagem, resposta)

        append_history(chat_id, "USER", mensagem)
        append_history(chat_id, "IA", resposta)

        return resposta
