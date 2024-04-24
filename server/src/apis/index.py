from fastapi import APIRouter
from src.apis.routes import users, threads, messages, patients_records

router = APIRouter(prefix="/apis", tags=["apis"])


router.include_router(users.router)
router.include_router(threads.router)
router.include_router(messages.router)
router.include_router(patients_records.router)
