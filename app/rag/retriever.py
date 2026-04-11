from supabase import create_client
from app.core.config import SUPABASE_URL, SUPABASE_KEY
import anthropic

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = anthropic.Anthropic()

def get_embedding(text: str) -> list:
    response = client.embeddings.create(
        model="voyage-3",
        input=text
    )
    return response.embeddings[0].embedding

def search_documents(query: str, business_id: str, limit: int = 5) -> list:
    embedding = get_embedding(query)
    
    result = supabase.rpc("match_documents", {
        "query_embedding": embedding,
        "match_business_id": business_id,
        "match_count": limit
    }).execute()
    
    return result.data