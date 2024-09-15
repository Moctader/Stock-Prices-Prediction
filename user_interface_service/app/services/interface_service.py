from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.financial_data import FinancialData
from app.core.logging import logger


class InterfaceService:
    async def get_data(self, code: str, db: AsyncSession):
        try:
            result = await db.execute(select(FinancialData).where(FinancialData.code == code))
            data = result.scalars().all()
            if not data:
                return None, f"No data found for {code}"
            logger.info(f"Data fetched successfully for code: {code}")
            return data, "Data fetched successfully"
        except Exception as e:
            logger.error(f"Error fetching data for code {code}: {e}")
            raise e
