# API de Chat com OpenAI (SSE)

Esta é uma API construída com FastAPI que permite interagir com o modelo GPT da OpenAI em tempo real usando Server-Sent Events (SSE).

## Requisitos

- Python 3.8+
- Chave de API da OpenAI

## Configuração

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Crie um arquivo `.env` na raiz do projeto e adicione sua chave da API:
```
OPENAI_API_KEY=sua_chave_api_aqui
```

## Executando a API

Para iniciar o servidor:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Interface Web

Ao acessar `http://localhost:8000`, você encontrará uma interface web amigável para interagir com o chat. A interface permite:

- Enviar mensagens para o ChatGPT
- Ver as respostas em tempo real (streaming)
- Histórico de mensagens na sessão atual

## Endpoints

### GET /
Retorna a interface web do chat

### GET /chat-stream
Endpoint SSE para streaming de respostas do ChatGPT.

Parâmetros de query:
- `prompt`: A mensagem a ser enviada para o ChatGPT

Exemplo de uso com JavaScript:
```javascript
const eventSource = new EventSource(`/chat-stream?prompt=Olá, como vai?`);

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'message') {
        console.log(data.content);
    }
};

eventSource.onerror = () => {
    eventSource.close();
};
```

## Documentação da API

Após iniciar o servidor, você pode acessar:
- Documentação Swagger UI: `http://localhost:8000/docs`
- Documentação ReDoc: `http://localhost:8000/redoc`

## Características

- Streaming de respostas em tempo real usando SSE
- Interface web responsiva
- Tratamento de erros robusto
- Documentação automática via Swagger/ReDoc 