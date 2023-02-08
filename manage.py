from threading import Thread
import requests


BASE_URL = 'https://www.binance.com/'
TICKER = 'XRPUSDT'
HOUR = 60 * 60 * 1000


def price_function() -> float:
    '''Returns ticker's price'''
    try:
        response = requests.get(
            f'{BASE_URL}fapi/v1/ticker/price?symbol={TICKER}'
        )
        response.raise_for_status()
        return float(response.json()['price'])
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)


def max_price_function() -> float:
    '''Returns maximum ticker's price for last hour'''
    import time
    now = int(time.time()*1000)
    try:
        response = requests.get(
            f'{BASE_URL}api/v3/klines?symbol={TICKER}&' +
            f'interval=1h&startTime={now-HOUR}&endTime={now}'
        )
        response.raise_for_status()
        return float(response.json()[0][2])
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(
                *self._args,
                ** self._kwargs
            )

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def main():
    while True:
        thread_1 = ThreadWithReturnValue(target=price_function)
        thread_2 = ThreadWithReturnValue(target=max_price_function)
        thread_1.start()
        thread_2.start()
        price = thread_1.join()
        max_price = thread_2.join()
        difference = (max_price - price) / max_price
        if difference > 0.0099:
            print('The price has fallen by more than 1% from the maximum')
            print(f'Current price of [{TICKER}] is {price}')
            print(f'Maximum price of [{TICKER}] for last hour is {max_price}')
            print(f'Difference is {"{:.4f}".format(difference * 100)}%')


if __name__ == '__main__':
    main()
