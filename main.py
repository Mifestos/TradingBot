import numpy as np
from pybit import exceptions
from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv, find_dotenv
from settings import symbol, kline_time, rsi_len, rsi_low, rsi_high
import asyncio
import talib
from orders import market_order, getPrecision

load_dotenv(find_dotenv())  # поиск .env с ключами

# создание сессии
session = HTTP(
    demo=True,
    #testnet=True,
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('SECRET_KEY')
)


async def run():  # асинхронная функция
    last_signal = None
    while True:  # бесконечный цикл в котором будем запрашивать свечи для анализа
        close_price = []

        response = session.get_kline(
            category="linear",  # фьючерсы
            symbol=symbol,  # валюта
            interval=kline_time,  # time frame
            limit=1000  # количество свеч
        )
        # сортировка свечей от самой старой к самой новой
        klines = response.get('result', {}).get('list', [])
        klines = sorted(klines, key=lambda x: int(x[0]))

        # получение списка цен закрытия свеч
        for candle in klines:
            close_price_for_list = float(candle[4])
            close_price.append(close_price_for_list)

        # конвертация в np список
        close_price = np.array(close_price, dtype='float')

        # импорт индикатора RSI
        rsi_value = talib.RSI(close_price, timeperiod=rsi_len)[-1]
        print(f"RSI: {round(rsi_value, 2)}")

        if rsi_value < rsi_low and last_signal != "Buy":
            """BUY"""
            await market_order(session, symbol, "Buy", close_price)
            last_signal = "Buy"
        elif rsi_value > rsi_high and last_signal != "Sell":
            """SELL"""
            await market_order(session, symbol, "Sell", close_price)
            last_signal = "Sell"

        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(run())
