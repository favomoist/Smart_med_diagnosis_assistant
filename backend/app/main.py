from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.engine.triage_engine import init_knowledge_base, seed_default_users
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables and seed knowledge base
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        init_knowledge_base(db)
        seed_default_users(db)
    finally:
        db.close()
    yield
    # Shutdown: cleanups if needed


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent symptom intake, red-flag emergency screening, and clinical triage decision-support API.",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/health", tags=["System Health"])
def health_check():
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }


# Include API v1 routes
app.include_router(api_router, prefix=settings.API_V1_STR)
