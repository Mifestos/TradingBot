# создание ордера
async def market_order(session, symbol, qty, side):
    market_order = session.place_order(
        category="linear",
        symbol=symbol,
        side=side,
        orderType="Market",
        qty=qty,
        timeInForce="PostOnly",
        orderFilter="Order"
    )
    print(market_order)


# подсчет знаков округления для qty
def getPrecision(symbol, session):
    response = session.get_instruments_info(
        category="linear",
        symbol=symbol
    )
    priceFilter = response['result']['list'][0]['priceFilter']
    lotSizeFilter = response['result']['list'][0]['lotSizeFilter']
    tickSize = priceFilter['tickSize']
    qtyStep = lotSizeFilter['qtyStep']

    if tickSize.startswith("0."):
        tickSize = tickSize.replace("0.", "")
    else:
        tickSize = str(float(tickSize))

    if qtyStep.startswith("0."):
        qtyStep = qtyStep.replace("0.")
    else:
        qtyStep = str(float(qtyStep))

    return int(len(qtyStep)), int(len(tickSize))