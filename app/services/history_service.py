import logging
from app.core.config import HISTORY_MAX_SIZE

historico_sessoes = {}

def get_history(chat_id):
    history = historico_sessoes.get(chat_id, [])
    logging.info(f"[{chat_id}] Histórico solicitado ({len(history)} mensagens)")
    return history

def append_history(chat_id, role, message):
    if chat_id not in historico_sessoes:
        logging.info(f"[{chat_id}] Novo histórico criado")
        historico_sessoes[chat_id] = []

    historico_sessoes[chat_id].append(f"{role}: {message}")
    logging.info(f"[{chat_id}] {role} adicionou mensagem: {message[:50]}...")

    if len(historico_sessoes[chat_id]) > HISTORY_MAX_SIZE:
        removed = historico_sessoes[chat_id].pop(0)
        logging.warning(f"[{chat_id}] Histórico excedeu limite. Removendo: {removed[:50]}...")
