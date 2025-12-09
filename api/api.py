from fastapi import FastAPI
from api.chat import router as chat_router
from api.random_parrot import router as random_parrot_router

app = FastAPI()


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


app.include_router(chat_router)
app.include_router(random_parrot_router)
