from fastapi import FastAPI

from app.api.items import router as items_router
from app.core.db import Base, engine
from app.api.digest import router as digest_router

app = FastAPI(title="Daily Notes Digest App")

Base.metadata.create_all(bind=engine)
app.include_router(items_router)
app.include_router(digest_router)

@app.get("/health")
def healthcheck():
    return {"status": "ok"}
