from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from app.db.session import get_db
from app.services.trend_service import TrendService
from app.core.logging import logger

router = APIRouter()
trend_service = TrendService()


@router.post("/analyze_trends")
async def analyze_trends(data: List[Dict[str, Any]], db: AsyncSession = Depends(get_db)):
    try:
        analysis_summary = await trend_service.process_data(data, db)
        if not analysis_summary:
            raise HTTPException(
                status_code=404, detail="Trend analysis failed")
        return analysis_summary
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
