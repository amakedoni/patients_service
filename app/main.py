from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.patients.router import router as patients_router

app = FastAPI(title="MAIsafe")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(patients_router, prefix="/api", tags=["DB"])
