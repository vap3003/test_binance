import time


BASE_URL = 'https://www.binance.com/'

ETH = 'ETHUSDT'
BTC = 'BTCUSDT'

HOUR = 60 * 60 * 1000

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS eth_token (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  time INTEGER,
  price FLOAT
);
"""

DELETE_OLD_DATA = f"""
    DELETE 
    FROM eth_token 
    WHERE time < {int(time.time()) - HOUR}
"""

SELECT_MIN_DATA = f"""
    SELECT MIN(price)
    FROM eth_token
    WHERE time > {int(time.time()) - HOUR}
"""

SELECT_MAX_DATA = f"""
    SELECT MAX(price)
    FROM eth_token
    WHERE time > {int(time.time()) - HOUR}
"""
