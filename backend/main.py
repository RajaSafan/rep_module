from fastapi import FastAPI

from backend.core.database import Base, engine
from backend.modules.representatives import models
from backend.modules.representatives.router import router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Representative Module API",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Representative Module API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
    }
    
    
    