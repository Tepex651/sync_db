from fastapi import APIRouter

from app.containers.info import InfoOut
from app.service.update import UpdateService

router = APIRouter()


@router.get("/info", response_model=InfoOut)
async def get_info():
    update_service = UpdateService()
    return await update_service.get_info()
