# API Python Chat

Backend em Python usando FastAPI para integração com a OpenAI e gerenciamento de streaming em tempo real.

## 🚀 Início Rápido

1. **Configure o ambiente virtual**
```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure o ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
PORT=8000
OPENAI_API_KEY=sua_chave_api_aqui
```

4. **Inicie o servidor**
```bash
# Desenvolvimento
uvicorn main:app --reload

# Produção
uvicorn main:app
```

## 📁 Estrutura

```
api-python-chat/
├── app/
│   ├── routes/
│   │   └── chat.py      # Rotas do chat
│   │   └── openai.py    # Serviço OpenAI
│   └── config.py        # Configurações
├── main.py              # Aplicação FastAPI
└── requirements.txt     # Dependências
```

## 🔌 API

### POST /chat
Endpoint para envio de mensagens ao chat.

**Request:**
```json
{
  "prompt": "string",    // Mensagem do usuário
  "userId": "string",    // ID do usuário (opcional)
  "userName": "string"   // Nome do usuário (opcional)
}
```

**Response:**
Stream de eventos (SSE) com o seguinte formato:
```
data: [chunk de resposta]
...
event: done
```

## ⚙️ Configuração

### Variáveis de Ambiente
- `PORT`: Porta do servidor (default: 8000)
- `OPENAI_API_KEY`: Chave de API da OpenAI

### CORS
Por padrão, o CORS está configurado para aceitar requisições de qualquer origem em desenvolvimento.
Para produção, configure as origens permitidas no arquivo `main.py`.

## 🔍 Logs
O servidor registra logs para:
- Requisições recebidas
- Respostas da OpenAI
- Erros e exceções

## 🔒 Segurança
- Validação de entrada usando Pydantic
- Sanitização de dados
- Proteção da chave da API
- Configuração de CORS

## 📝 Dependências Principais

- FastAPI: Framework web moderno e rápido
- uvicorn: Servidor ASGI para Python
- python-dotenv: Gerenciamento de variáveis de ambiente
- openai: SDK oficial da OpenAI
- pydantic: Validação de dados

## 🔧 Desenvolvimento

### Instalando novas dependências
```bash
pip install nome-do-pacote
pip freeze > requirements.txt
```

### Testes
```bash
# Instale o pytest
pip install pytest

# Execute os testes
pytest
```

### Documentação da API
Após iniciar o servidor, acesse:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📦 Deploy

1. **Prepare o ambiente**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure as variáveis de ambiente**
```bash
export PORT=8000
export OPENAI_API_KEY=sua_chave_api_aqui
```

3. **Inicie o servidor**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## ⚠️ Tratamento de Erros

O sistema inclui tratamento para:
- Erros de validação de entrada
- Falhas na API da OpenAI
- Timeouts de conexão
- Erros de streaming 