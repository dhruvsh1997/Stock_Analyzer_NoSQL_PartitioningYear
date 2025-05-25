import requests
from pymongo import MongoClient
from datetime import datetime
import logging
import os

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'stock_analyzer.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_store_stock(symbol):
    try:
        API_KEY = 'X32JAFMLTTVA0838'
        # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&interval=5min&apikey={API_KEY}&outputsize=compact"
        res = requests.get(url)
        data = res.json()
        logging.info(f"Getting the data for : {symbol}")
        if 'Time Series (Daily)' not in data:
            logging.warning(f"No data found for symbol: {symbol}")
            return

        client = MongoClient("mongodb://localhost:27017/")
        series = data['Time Series (Daily)']
        logging.info(f"Getting data series : {series}")

        for date_str, values in series.items():
            year = datetime.strptime(date_str, "%Y-%m-%d").year
            db = client[f"stock_data_{year}"]
            record = {
                "symbol": symbol,
                "date": date_str,
                "open": float(values['1. open']),
                "high": float(values['2. high']),
                "low": float(values['3. low']),
                "close": float(values['4. close']),
                "volume": int(values['5. volume'])
            }
            db[symbol].insert_one(record)

        logging.info(f"Inserted records for symbol: {symbol}")

    except Exception as e:
        logging.error(f"Error in fetch_and_store_stock for {symbol}: {str(e)}")