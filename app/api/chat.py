from fastapi import APIRouter
from pydantic import BaseModel
import anthropic
from app.core.config import ANTHROPIC_API_KEY
from app.rag.retriever import ingest_text, search_documents

router = APIRouter()
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

class ChatRequest(BaseModel):
    message: str
    business_id: str = "demo"

class IngestRequest(BaseModel):
    text: str
    business_id: str = "demo"

@router.post("/chat")
def chat(request: ChatRequest):
    # Buscar contexto relevante en Supabase
    docs = search_documents(request.message, request.business_id)
    context = "\n".join([d["content"] for d in docs]) if docs else ""

    system_prompt = f"""Sos Orbi, un asistente virtual inteligente para negocios.
Respondés preguntas de clientes de forma amable, clara y concisa.
Usá únicamente la información del negocio que te damos a continuación para responder.
Si no encontrás la respuesta en esa información, decilo honestamente.

Información del negocio:
{context}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": request.message}
        ]
    )
    return {"response": response.content[0].text}

@router.post("/ingest")
def ingest(request: IngestRequest):
    ingest_text(request.text, request.business_id)
    return {"status": "ok", "message": "Texto ingresado correctamente"}