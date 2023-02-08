
# Tracker of ticker price on Binance

Code track changings of XRP/USDT price and compare it with the highest price for last hour. In case, when difference reach 1%, program sent message to console.


## Run Locally

Clone the project

```bash
  git clone git@github.com:vap3003/test_binance.git
```

Go to the project directory

```bash
  cd test_binance
```

Create and activate Virtual Environments

```bash
  python3 -m venv venv
  source venv/bin/activate
```

Install dependencies

```bash
  pip install -r Requirments.txt
```

Start the project

```bash
  python manage.py 
```


## How to track all tickers

- To learn API documentation about getting response with list of tickers in one request
- To optimize the frequency of maximum ticker's cost requests to reduce operating time
- To use Threading or Multiprocessing



## Author

- [@vap3003](https://www.github.com/vap3003)
