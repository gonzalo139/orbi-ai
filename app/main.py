from fastapi import FastAPI
from app.api.chat import router

app = FastAPI(title="Orbi API")

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Orbi is alive 🟢"}