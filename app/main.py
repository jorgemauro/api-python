from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json
import httpx
from openai import AsyncOpenAI
import logging
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega as variáveis de ambiente
load_dotenv()

# Modelo para a requisição
class ChatRequest(BaseModel):
    prompt: str
    userId: str | None = None
    userName: str | None = None

# Cliente HTTP personalizado
@asynccontextmanager
async def get_openai_client():
    async with httpx.AsyncClient(
        base_url="https://api.openai.com/v1",
        timeout=None,
        follow_redirects=True,
        headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}
    ) as client:
        yield AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            http_client=client
        )

# Configuração da API
app = FastAPI(
    title="Chat API",
    description="API para interação com ChatGPT usando SSE",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta os arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

async def stream_generator(prompt: str, userId: str | None = None, userName: str | None = None):
    try:
        logger.info(f"Iniciando streaming para usuário {userName} (ID: {userId})")
        logger.info(f"Prompt: {prompt}")
        
        messages = [{"role": "user", "content": prompt}]
        if userName:
            messages.insert(0, {"role": "system", "content": f"O usuário se chama {userName}. Seja amigável e use o nome dele quando apropriado."})

        async with get_openai_client() as client:
            stream = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    logger.info(f"Chunk recebido: {content}")
                    yield f"data: {content}\n\n"
            
            # Envia evento de conclusão
            yield "event: done\n\n"
            
    except Exception as e:
        logger.error(f"Erro ao processar chat: {str(e)}")
        yield f"event: error\ndata: {str(e)}\n\n"

@app.post("/chat")
async def chat(request: ChatRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt é obrigatório.")
    
    logger.info(f"Nova requisição recebida de {request.userName} (ID: {request.userId})")
    return StreamingResponse(
        stream_generator(request.prompt, request.userId, request.userName),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("app/static/index.html")

@app.get("/chat-page", response_class=HTMLResponse)
async def chat_page():
    return FileResponse("app/static/chat.html") 