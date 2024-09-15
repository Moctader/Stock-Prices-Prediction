import aiohttp
from app.core.settings import settings
from app.core.logging import logger


async def fetch_financial_data(symbol: str):
    url = f"https://eodhd.com/api/eod-bulk-last-day/US?api_token={settings.API_KEY}&fmt=json&symbols={symbol}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                logger.info(f"Successfully fetched data for symbol: {symbol}")
                return data
            else:
                logger.error(
                    f"Failed to fetch data for symbol: {symbol}, status code: {response.status}")
    return None
