from fastapi import APIRouter

from app.routes.auth import router
from app.db import Base, engine

api = APIRouter()

# bazadagi jadvallarni yaratish uchun
Base.metadata.create_all(bind=engine)

api.include_router(router)
