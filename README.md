# **Projeto ChatBot IA | FastAPI + Ollama**

Este projeto consiste em uma API de chatbot desenvolvida como desafio técnico. O sistema utiliza modelos de linguagem locais (LLM) para processar perguntas e manter conversas contextuais com alta performance.


* **FastAPI**: Framework moderno e assíncrono para a API.
* **LangChain**: Orquestração do fluxo de conversa e gerenciamento de templates.
* **Ollama**: Execução local do modelo `llama3.2:1b`

---

## **Funcionalidades**

* Chat com IA usando modelos Ollama
* Histórico persistente por `chat_id`
* Cache LRU para respostas repetidas
* Arquitetura modular (core, services, routes, models)1
* Logging automático para debug
* Configurações via `config.py`
* Documentação automática em `/docs`

---

## **Estrutura do Projeto**

```
app/
├── api/
│   └── routes/
│       └── chat_routes.py
├── core/
│   ├── config.py
│   └── logger.py
├── models/
│   └── chat_models.py
├── services/
│   └── chat_service.py
└── main.py
```

---

## **Instalação**

### 1. Clone o repositório

```bash
git clone https://github.com/YuriAbbud/chatbot-api
cd chatbot-api
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Instalando e executando o modelo Ollama

Baixe o modelo recomendado:

```bash
ollama pull llama3.2:1b
```

Execute:

```bash
ollama run llama3.2:1b
```

---

##  **Executando o servidor**

```bash
uvicorn app.main:app --reload
```

Acesse:

```
http://127.0.0.1:8000/docs
```

### Exemplos de curl 
```
curl -X POST "http://127.0.0.1:8000/chat/" \
     -H "Content-Type: application/json" \
     -d '{"mensagem": "Olá API, como vai?"}'
```

---

## **Endpoints**

### POST `/chat/`

Envia uma mensagem para o chatbot.

#### Body:

```json
{
  "mensagem": "Olá"
}
```

#### Headers opcionais:

```
chat_id: <ID do chat>
```

#### Exemplo de resposta:

```json
{
  "resposta": "Olá! Como posso ajudar?",
  "chat_id": "fe2c2a9b-..."
}
```

---

### GET `/chat/{chat_id}`

Retorna o histórico completo da sessão.

---
Feito por Yuri Ravagnani Abbud, 22 de novembro de 2025.

Chat com Gemini: https://gemini.google.com/share/fe139de5db62