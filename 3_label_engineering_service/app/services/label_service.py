from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import tuple_
from app.core.logging import logger
import pandas as pd
from typing import List, Dict, Any
from app.db.models.stock_price import StockPrice


class LabelService:
    async def process_data(self, data: List[Dict[str, Any]], db: AsyncSession):
        try:
            # Convert input time series data to DataFrame
            df = pd.DataFrame(data)

            # Ensure 'date' column is in datetime format
            if df['date'].dtype == object:
                df['date'] = pd.to_datetime(df['date'])

            # Apply label engineering
            # Example label: next day's closing price
            df['future_price'] = df['close'].shift(-1)
            df['price_increase'] = (df['future_price'] > df['close']).astype(
                int)  # Binary label for price increase

            # Drop rows where 'future_price' is NaN
            df.dropna(subset=['future_price'], inplace=True)

            processed_data = df.to_dict(orient="records")
            logger.info("Data processed successfully")

            # Save to database with duplicate check
            await self.save_to_db(processed_data, db)

            return processed_data
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            raise e

    async def save_to_db(self, data: List[Dict[str, Any]], db: AsyncSession):
        try:
            # Check for duplicates
            existing_records = await self.get_existing_records(data, db)
            existing_keys = {(record.code, record.date)
                             for record in existing_records}

            # Filter out duplicates
            new_data = [item for item in data if (
                item['code'], item['date']) not in existing_keys]

            if new_data:
                # Convert list of dictionaries to list of StockPrice instances
                db_data = [StockPrice(
                    code=item['code'],
                    exchange_short_name=item.get('exchange_short_name', 'N/A'),
                    date=item['date'],
                    open=item.get('open', 0.0),
                    high=item.get('high', 0.0),
                    low=item.get('low', 0.0),
                    close=item.get('close', 0.0),
                    adjusted_close=item.get('adjusted_close', 0.0),
                    volume=item.get('volume', 0),
                    prev_close=item.get('prev_close', 0.0),
                    change=item.get('change', 0.0),
                    change_p=item.get('change_p', 0.0),
                    mid_price=item.get('mid_price', 0.0),
                    volatility=item.get('volatility', 0.0),
                    future_price=item.get('future_price', 0.0),
                    price_increase=item.get('price_increase', 0)
                ) for item in new_data]

                # Add all instances to the session
                db.add_all(db_data)
                await db.commit()

                # Refresh instances to get updated data from the database
                for record in db_data:
                    await db.refresh(record)

                logger.info("Data saved to the database successfully")
            else:
                logger.info("No new data to save")
        except Exception as e:
            await db.rollback()
            logger.error(f"Error saving data to the database: {e}")
            raise e

    async def get_existing_records(self, data: List[Dict[str, Any]], db: AsyncSession):
        codes_dates = [(item['code'], item['date']) for item in data]

        query = select(StockPrice).filter(
            tuple_(StockPrice.code, StockPrice.date).in_(codes_dates)
        )

        result = await db.execute(query)
        return result.scalars().all()
