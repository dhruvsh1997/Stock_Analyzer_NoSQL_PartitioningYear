# 🧠 Stock Analyzer (MongoDB Partitioning by Year)

This project fetches historical stock data from Alpha Vantage, partitions it in MongoDB by year, and allows you to visualize it via a Django web app. It uses Celery for background task processing and Docker for containerized deployment.

---

## 🚀 Features
- Fetch daily stock prices (AAPL, NVDA, etc.) via Alpha Vantage API
- Partitioned MongoDB storage (e.g., `stock_data_2024`)
- Asynchronous background fetching via Celery
- Docker + RabbitMQ + MongoDB setup

---

## 📦 Project Structure
```
.
├── market/             # Django app
├── stock_analyzer/     # Project config
├── templates/
├── static/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔧 How to Run (Docker)
```bash
docker-compose up --build
```

- App: http://localhost:8000
- RabbitMQ Admin: http://localhost:15672  (user: guest / pass: guest)
- MongoDB: localhost:27017

---

## ⚙️ How to Run (Local, No Docker)
```bash
# 1. Start MongoDB and RabbitMQ
sudo systemctl start mongod
sudo systemctl start rabbitmq-server

# 2. Setup Python venv
python3 -m venv env && source env/bin/activate
pip install -r requirements.txt

# 3. Run Django server
python manage.py runserver

# 4. Start Celery worker (in another terminal)
celery -A stock_analyzer worker --loglevel=info
```

---

## 🔑 API Key Setup
Update your Alpha Vantage key in `market/utils.py`:
```python
API_KEY = 'YOUR_ALPHA_VANTAGE_KEY'
```

---

## 🧪 Test URLs
```url
http://localhost:8000/?symbol=AAPL&year=2024
```

---

## ✅ To Do
- [ ] Chart.js integration
- [ ] Celery beat scheduler for auto-daily fetch
- [ ] Email alerts/log viewer for failures

---

## 📃 License
MIT License

celery -A stock_analyzer worker --loglevel=INFO --pool=solo -n worker1@%h