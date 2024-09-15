from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from app.db.session import get_db
from app.services.label_service import LabelService
from app.core.logging import logger

router = APIRouter()
label_service = LabelService()


@router.post("/label_engineering")
async def process_data(data: List[Dict[str, Any]], db: AsyncSession = Depends(get_db)):
    try:
        processed_data = await label_service.process_data(data, db)
        if not processed_data:
            raise HTTPException(
                status_code=404, detail="Data processing failed")
        return processed_data
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
