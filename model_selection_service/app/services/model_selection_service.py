from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import tuple_
from app.core.logging import logger
import pandas as pd
from typing import List, Dict, Any
from app.db.models.stock_price import StockPrice
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import datetime


class ModelSelectionService:
    async def process_data(self, data: List[Dict[str, Any]], db: AsyncSession):
        try:
            # Convert input time series data to DataFrame
            df = pd.DataFrame(data)

            # Ensure 'date' column is in datetime format
            if df['date'].dtype == object:
                df['date'] = pd.to_datetime(df['date'])

            # Normalize data
            df = self.normalize_data(
                df, ['open', 'high', 'low', 'close', 'adjusted_close', 'volume'])

            # Split data into train, validation, and test sets
            train_data, val_data, test_data = self.split_data(df)

            # Save data to database
            await self.save_to_db(train_data, db, 'train')
            await self.save_to_db(val_data, db, 'validation')
            await self.save_to_db(test_data, db, 'test')

            all_data = df.to_dict(orient="records")
            train_data_list = train_data.to_dict(orient="records")
            val_data_list = val_data.to_dict(orient="records")
            test_data_list = test_data.to_dict(orient="records")

            logger.info("Data processed and stored successfully")
            return {"data": all_data, "train_data": train_data_list, "val_data": val_data_list, "test_data": test_data_list}
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            raise e

    def normalize_data(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        scaler = StandardScaler()
        df[columns] = scaler.fit_transform(df[columns])
        logger.info("Data normalized")
        return df

    def split_data(self, df: pd.DataFrame, test_size: float = 0.2, val_size: float = 0.1):
        train_val_data, test_data = train_test_split(
            df, test_size=test_size, shuffle=True, random_state=42)
        train_data, val_data = train_test_split(
            train_val_data, test_size=val_size/(1-test_size), shuffle=True, random_state=42)
        logger.info("Data split into train, validation, and test sets")
        return train_data, val_data, test_data

    async def save_to_db(self, df: pd.DataFrame, db: AsyncSession, dataset_type: str):
        try:
            version = datetime.datetime.utcnow().isoformat()
            new_data = []
            existing_records = await self.get_existing_records(df.to_dict(orient='records'), db)
            existing_keys = {(record.code, record.date)
                             for record in existing_records}

            for item in df.to_dict(orient='records'):
                if (item['code'], item['date']) not in existing_keys:
                    new_data.append(StockPrice(
                        code=item['code'],
                        exchange_short_name=item.get(
                            'exchange_short_name', 'N/A'),
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
                        price_increase=item.get('price_increase', 0),
                        version=version,
                        dataset_type=dataset_type
                    ))

            if new_data:
                db.add_all(new_data)
                await db.commit()
                for record in new_data:
                    await db.refresh(record)
                logger.info(
                    f"{dataset_type.capitalize()} data saved to the database successfully")
            else:
                logger.info(f"No new {dataset_type} data to save")
        except Exception as e:
            await db.rollback()
            logger.error(
                f"Error saving {dataset_type} data to the database: {e}")
            raise e

    async def get_existing_records(self, data: List[Dict[str, Any]], db: AsyncSession):
        codes_dates = [(item['code'], item['date']) for item in data]
        query = select(StockPrice).filter(
            tuple_(StockPrice.code, StockPrice.date).in_(codes_dates))
        result = await db.execute(query)
        return result.scalars().all()
