from fastapi import APIRouter
from app.api.v1 import auth, profiles, knowledge, triage, share

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Accounts"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["Patient & Dependent Profiles"])
api_router.include_router(triage.router, prefix="/triage", tags=["Symptom Intake & Triage"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Clinical Knowledge Base"])
api_router.include_router(share.router, prefix="/share", tags=["Clinician Summary Sharing"])
