from pybit import exceptions
from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv, find_dotenv
from settings import symbol, kline_time
import asyncio

load_dotenv(find_dotenv())
session = HTTP(
    testnet=True,
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('SECRET_KEY')
)

if __name__ == '__main__':
    asyncio.run()