from django.shortcuts import render
from pymongo import MongoClient
from datetime import datetime
import logging
import os
from .tasks import fetch_stock_task  # Import the Celery task

# Logger setup
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'stock_analyzer.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PREDEFINED_SYMBOLS = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'INTC', 'IBM']
CURRENT_YEAR = datetime.now().year
YEARS = [str(CURRENT_YEAR - i) for i in range(5)]

def index(request):
    try:
        if request.method == 'POST':
            symbol = request.POST.get('symbol', 'AAPL').upper()
            year = request.POST.get('year', str(CURRENT_YEAR))
        else:
            symbol = request.GET.get('symbol', 'AAPL').upper()
            year = request.GET.get('year', str(CURRENT_YEAR))

        # Trigger Celery async task to fetch and store stock data
        fetch_stock_task.delay(symbol)

        client = MongoClient("mongodb://localhost:27017/")
        db = client[f"stock_data_{year}"]
        records = list(db[symbol].find().sort("date", -1))
        logging.info(f"Fetched {len(records)} records for {symbol} in {year}.")

    except Exception as e:
        logging.error(f"Error in index view for {symbol} in {year}: {str(e)}")
        records = []

    return render(request, 'index.html', {
        'records': records,
        'symbol': symbol,
        'year': year,
        'symbols': PREDEFINED_SYMBOLS,
        'years': YEARS
    })
