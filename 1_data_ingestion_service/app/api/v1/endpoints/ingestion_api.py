from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.ingestion_service import IngestionService
from app.core.logging import logger

router = APIRouter()
ingestion_service = IngestionService()


@router.post("/ingest_data")
async def ingest_data(code: str = 'EURUSD.FOREX', db: AsyncSession = Depends(get_db)):
    try:
        financial_data, message = await ingestion_service.ingest_data(code, db)
        if not financial_data:
            raise HTTPException(status_code=404, detail=message)
        return {"message": message}
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/ingest")
async def get_all_ingested_data(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000)
):
    try:
        financial_data_list = await ingestion_service.get_all_data(db, page, page_size)
        return financial_data_list
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
