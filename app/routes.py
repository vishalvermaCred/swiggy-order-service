from fastapi.params import Body
from fastapi import APIRouter
from fastapi.logger import logger

from app.models import PlaceOrder
from app.service import process_order
from app.utils import generate_response

router = APIRouter()

LOGGER_KEY = "app.router"


@router.get("/public/healthz")
async def health_check():
    """
    health api of order service to check if order service is working fine or not.
    """
    return {"message": "OK"}


@router.post("/place-order")
async def place_order(body: PlaceOrder = Body(...)):
    logger.info(f"{LOGGER_KEY}.place_order")
    response = await process_order(body.dict())
    return await generate_response(**response)
