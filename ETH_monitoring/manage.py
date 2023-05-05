import requests
import settings
from db_utils import (create_connection, execute_query, fetch_query,
                      insert_price)


def price_function():
    '''Returns ticker's prices from Binance API'''
    try:
        response = requests.get(f'{settings.BASE_URL}api/v3/ticker/price?'
                                f'symbols=[%22{settings.ETH}%22,'
                                f'%22{settings.BTC}%22]')
        response.raise_for_status()
        return [
            float(response.json()[1]['price']),
            float(response.json()[0]['price'])
        ]
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)


def main():
    connection = create_connection('ETH_monitoring/db/token.sqlite')
    execute_query(connection, settings.CREATE_TABLE)
    execute_query(connection, settings.DELETE_OLD_DATA)
    print('Checking has been started.')
    prev_eth, prev_btc = price_function()
    clear_eth = prev_eth
    while True:
        cur_eth, cur_btc = price_function()
        if (cur_btc - prev_btc) * (cur_eth - prev_eth) > 0:
            clear_eth += (cur_eth - prev_eth)*0.45
        else:
            clear_eth += (cur_eth - prev_eth)/0.45
        prev_eth, prev_btc = cur_eth, cur_btc
        execute_query(
            connection,
            insert_price(clear_eth))
        max_price = fetch_query(
            connection,
            settings.SELECT_MAX_DATA)[0][0]
        min_price = fetch_query(
            connection,
            settings.SELECT_MIN_DATA)[0][0]
        if ((max_price - clear_eth) / max_price) > 0.0099:
            print('Clear price has decreased by more than 1%')
            print(f'Current clear price of [{settings.ETH}] is {clear_eth}')
            print(f'Maximum price of [{settings.ETH}] \
                   for last hour is {min_price}')
        if ((clear_eth - min_price) / min_price) > 0.0099:
            print('Clear price has increased by more than 1%')
            print(f'Current clear price of [{settings.ETH}] is {clear_eth}')
            print(f'Minimum price of [{settings.ETH}] \
                   for last hour is {min_price}')


if __name__ == '__main__':
    main()
