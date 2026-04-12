from supabase import create_client
from app.core.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

_model = None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def get_embedding(text: str) -> list:
    embedding = get_model().encode(text)
    return embedding.tolist()

def search_documents(query: str, business_id: str, limit: int = 5) -> list:
    embedding = get_embedding(query)
    result = supabase.rpc("match_documents", {
        "query_embedding": embedding,
        "match_business_id": business_id,
        "match_count": limit
    }).execute()
    return result.data

def ingest_text(text: str, business_id: str, metadata: dict = {}) -> None:
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    for chunk in chunks:
        embedding = get_embedding(chunk)
        supabase.table("documents").insert({
            "business_id": business_id,
            "content": chunk,
            "embedding": embedding,
            "metadata": metadata
        }).execute()