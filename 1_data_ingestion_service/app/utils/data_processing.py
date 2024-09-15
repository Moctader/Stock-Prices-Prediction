import aiohttp
import asyncio
from app.core.settings import settings
from app.core.logging import logger
from aiohttp import ClientError


async def fetch_financial_data(symbol: str, max_retries: int = 5, retry_delay: int = 2):
    url = f"https://eodhd.com/api/intraday/{symbol}?api_token={settings.API_KEY}&fmt=json"

    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(
                            f"Successfully fetched data for symbol: {symbol}")
                        return data
                    else:
                        logger.error(
                            f"Failed to fetch data for symbol: {symbol}, status code: {response.status}")
        except ClientError as e:
            logger.error(
                f"Client error fetching data for symbol: {symbol}, error: {str(e)}")
        except Exception as e:
            logger.error(
                f"Unexpected error fetching data for symbol: {symbol}, error: {str(e)}")

        logger.info(
            f"Retrying fetch for symbol: {symbol} in {retry_delay} seconds...")
        await asyncio.sleep(retry_delay)

    logger.error(
        f"Failed to fetch data for symbol: {symbol} after {max_retries} attempts")
    return None
