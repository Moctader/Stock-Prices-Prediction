from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
import pandas as pd
from typing import List, Dict, Any
from app.db.models.stock_analysis import StockAnalysis
from sklearn.preprocessing import StandardScaler
# import vectorbt as vbt


class AnalysisService:
    async def process_data(self, data: List[Dict[str, Any]], db: AsyncSession):
        try:
            # Convert input time series data to DataFrame
            df = pd.DataFrame(data)

            # Ensure 'date' column is in datetime format
            if df['date'].dtype == object:
                df['date'] = pd.to_datetime(df['date'])

            # Normalize data
            df = self.normalize_data(df, ['close'])

            # Perform trend analysis
            analysis_summary = await self.analyze_trends(df, db)

            return analysis_summary
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            raise e

    def normalize_data(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        scaler = StandardScaler()
        df[columns] = scaler.fit_transform(df[columns])
        logger.info("Data normalized")
        return df

    async def analyze_trends(self, df: pd.DataFrame, db: AsyncSession):
        try:
            df.set_index('date', inplace=True)

            # Generate signals for backtesting
            entries = df['close'] > df['close'].shift(1)
            exits = df['close'] < df['close'].shift(1)

            # Perform backtesting using vectorbt
            # pf = vbt.Portfolio.from_signals(df['close'], entries, exits)

            # Calculate performance metrics
            total_return = 0.0  # pf.total_return()
            average_return = 0.0  # pf.annualized_return()
            volatility = 0.0  # pf.annualized_volatility()
            sharpe_ratio = ""  # pf.sharpe_ratio()

            # Log the metrics
            logger.info(f"Total Return: {total_return}")
            logger.info(f"Average Return: {average_return}")
            logger.info(f"Volatility: {volatility}")
            logger.info(f"Sharpe Ratio: {sharpe_ratio}")

            # Save trend analysis results to database
            analysis_records = []
            for date, close in zip(df.index, df['close']):
                # Replace the following placeholders with actual calculations
                return_ = float(total_return)
                sma_10 = float(average_return)
                sma_50 = float(volatility)
                trend = str(sharpe_ratio)

                analysis_record = StockAnalysis(
                    date=date,
                    close=close,
                    return_=return_,
                    sma_10=sma_10,
                    sma_50=sma_50,
                    trend=trend
                )
                analysis_records.append(analysis_record)

            await self.bulk_save_data(analysis_records, db)
            logger.info(
                "Trend analysis results saved to database successfully.")

            summary = {
                "total_return": total_return,
                "average_return": average_return,
                "volatility": volatility,
                "sharpe_ratio": sharpe_ratio
            }
            return summary
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            raise e

    async def bulk_save_data(self, data: List[StockAnalysis], db: AsyncSession, batch_size: int = 100):
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

            logger.info("Data saved to the database successfully.")
        except Exception as e:
            await db.rollback()
            logger.error(f"Error saving data to the database: {e}")
            raise e
