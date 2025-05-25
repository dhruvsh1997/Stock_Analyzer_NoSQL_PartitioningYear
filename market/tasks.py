from celery import shared_task
from .utils import fetch_and_store_stock

@shared_task
def fetch_stock_task(symbol):
    fetch_and_store_stock(symbol)
    return "sucess"