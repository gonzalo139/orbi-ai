from fastapi import APIRouter
from pydantic import BaseModel
import anthropic
from app.core.config import ANTHROPIC_API_KEY
from app.rag.retriever import search_documents, ingest_text

router = APIRouter()
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    business_id: str = "demo"
    history: list[Message] = []

class IngestRequest(BaseModel):
    text: str
    business_id: str = "demo"

@router.post("/chat")
def chat(request: ChatRequest):
    docs = search_documents(request.message, request.business_id)
    context = "\n".join([d["content"] for d in docs]) if docs else ""

    system_prompt = f"""Sos Orbi, el asistente virtual de La Parrilla Don Carlos.
Respondés las consultas de los clientes de forma amable, cálida y concisa, como lo haría un mozo atento.
Usá únicamente la información del restaurante que se detalla a continuación.
Si alguien pregunta algo que no está en esa información, decilo con naturalidad y sugerí que llamen al restaurante.
No inventes precios ni datos que no estén en el contexto.

{context}"""

    messages = [{"role": m.role, "content": m.content} for m in request.history]
    messages.append({"role": "user", "content": request.message})

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=system_prompt,
        messages=messages
    )

    return {"response": response.content[0].text}

@router.post("/ingest")
def ingest(request: IngestRequest):
    ingest_text(request.text, request.business_id)
    return {"status": "ok", "message": "Texto ingresado correctamente"}
