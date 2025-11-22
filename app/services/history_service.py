from app.core.config import HISTORY_MAX_SIZE

historico_sessoes = {}

def get_history(chat_id):
    return historico_sessoes.get(chat_id, [])

def append_history(chat_id, role, message):
    if chat_id not in historico_sessoes:
        historico_sessoes[chat_id] = []

    historico_sessoes[chat_id].append(f"{role}: {message}")

    if len(historico_sessoes[chat_id]) > HISTORY_MAX_SIZE:
        historico_sessoes[chat_id].pop(0)
