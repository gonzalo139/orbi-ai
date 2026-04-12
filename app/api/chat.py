from fastapi import APIRouter
from pydantic import BaseModel
import anthropic
from app.core.config import ANTHROPIC_API_KEY

router = APIRouter()
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

class ChatRequest(BaseModel):
    message: str
    business_id: str = "demo"

@router.post("/chat")
def chat(request: ChatRequest):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="""Sos Orbi, un asistente virtual inteligente para negocios.
Respondés preguntas de clientes de forma amable, clara y concisa.
Si no sabés algo, lo decís honestamente.""",
        messages=[
            {"role": "user", "content": request.message}
        ]
    )
    
    return {"response": response.content[0].text}

from app.rag.retriever import ingest_text, search_documents

class IngestRequest(BaseModel):
    text: str
    business_id: str = "demo"

@router.post("/ingest")
def ingest(request: IngestRequest):
    ingest_text(request.text, request.business_id)
    return {"status": "ok", "message": "Texto ingresado correctamente"}