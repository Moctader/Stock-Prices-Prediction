from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.interface_service import InterfaceService
from app.core.logging import logger

router = APIRouter()
interface_service = InterfaceService()


@router.get("/data/aapl")
async def get_aapl_data(db: AsyncSession = Depends(get_db)):
    try:
        data, message = await interface_service.get_data("AAPL", db)
        if not data:
            raise HTTPException(status_code=404, detail=message)
        return data
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/data/msft")
async def get_msft_data(db: AsyncSession = Depends(get_db)):
    try:
        data, message = await interface_service.get_data("MSFT", db)
        if not data:
            raise HTTPException(status_code=404, detail=message)
        return data
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/data/googl")
async def get_googl_data(db: AsyncSession = Depends(get_db)):
    try:
        data, message = await interface_service.get_data("GOOGL", db)
        if not data:
            raise HTTPException(status_code=404, detail=message)
        return data
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/data/amzn")
async def get_amzn_data(db: AsyncSession = Depends(get_db)):
    try:
        data, message = await interface_service.get_data("AMZN", db)
        if not data:
            raise HTTPException(status_code=404, detail=message)
        return data
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/data/tsla")
async def get_tsla_data(db: AsyncSession = Depends(get_db)):
    try:
        data, message = await interface_service.get_data("TSLA", db)
        if not data:
            raise HTTPException(status_code=404, detail=message)
        return data
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/data/fb")
async def get_fb_data(db: AsyncSession = Depends(get_db)):
    try:
        data, message = await interface_service.get_data("FB", db)
        if not data:
            raise HTTPException(status_code=404, detail=message)
        return data
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
