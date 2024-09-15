from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.stock_price import StockPrice
from app.utils.data_processing import fetch_financial_data
from app.utils.parsers import parse_float, parse_int, parse_date
from app.core.logging import logger
from typing import List, Dict, Any


class IngestionService:
    async def ingest_data(self, code: str, db: AsyncSession, batch_size: int = 100):
        try:
            data_list = await fetch_financial_data(code)
            if not data_list:
                return None, "Data not found"

            # Fetch existing dates for the given code
            existing_dates = await self.get_existing_dates(code, db)

            new_records = []
            for data in data_list:
                date_value = data.get('date') or data.get('datetime')
                parsed_date = parse_date(date_value)

                if parsed_date is None:
                    logger.error(
                        f"Skipping data with invalid date: {date_value}")
                    continue

                if parsed_date in existing_dates:
                    logger.info(
                        f"Data for {code} on {parsed_date} already exists, skipping insertion.")
                    continue

                financial_data = StockPrice(
                    code=code,
                    exchange_short_name=data.get('exchange_short_name', 'N/A'),
                    date=parsed_date,
                    open=parse_float(data.get('open', 0.0)),
                    high=parse_float(data.get('high', 0.0)),
                    low=parse_float(data.get('low', 0.0)),
                    close=parse_float(data.get('close', 0.0)),
                    adjusted_close=parse_float(
                        data.get('adjusted_close', 0.0)),
                    volume=parse_int(data.get('volume', 0)),
                    prev_close=parse_float(data.get('prev_close', 0.0)),
                    change=parse_float(data.get('change', 0.0)),
                    change_p=parse_float(data.get('change_p', 0.0)),
                )

                new_records.append(financial_data)
                existing_dates.add(parsed_date)

            # Save new records in bulk if there are any
            if new_records:
                await self.bulk_save_data(new_records, db, batch_size)
                logger.info(f"Data ingested successfully for code: {code}")
                return new_records, "Data ingested successfully"
            else:
                logger.info(f"No new data to ingest for code: {code}")
                return None, "No new data to ingest"
        except Exception as e:
            await db.rollback()
            logger.error(f"Error ingesting data for code {code}: {e}")
            raise e

    async def get_existing_dates(self, code: str, db: AsyncSession):
        try:
            result = await db.execute(
                select(StockPrice.date).where(StockPrice.code == code)
            )
            existing_dates = {record for record in result.scalars().all()}
            logger.info(f"Existing dates for {code}: {existing_dates}")
            return existing_dates
        except Exception as e:
            logger.error(f"Error fetching existing dates for code {code}: {e}")
            raise e

    async def bulk_save_data(self, data: List[StockPrice], db: AsyncSession, batch_size: int = 100):
        try:
            new_records = []
            for record in data:
                new_records.append(record)
                if len(new_records) >= batch_size:
                    db.add_all(new_records)
                    await db.commit()
                    for record in new_records:
                        await db.refresh(record)
                    new_records = []

            if new_records:
                db.add_all(new_records)
                await db.commit()
                for record in new_records:
                    await db.refresh(record)

            logger.info("Data saved to the database successfully")
        except Exception as e:
            await db.rollback()
            logger.error(f"Error saving data to the database: {e}")
            raise e

    async def get_all_data(self, db: AsyncSession, page: int = 1, page_size: int = 100):
        try:
            offset = (page - 1) * page_size
            result = await db.execute(
                select(StockPrice)
                .order_by(StockPrice.date)
                .offset(offset)
                .limit(page_size)
            )
            financial_data_list = result.scalars().all()
            logger.info(f"Fetched page {page} of ingested data successfully")
            return financial_data_list
        except Exception as e:
            logger.error(f"Error fetching data for page {page}: {e}")
            raise e
