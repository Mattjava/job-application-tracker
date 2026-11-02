from flask import Flask
from dotenv import load_dotenv
import mysql.connector, os

load_dotenv()

config = {
    "host": "localhost",
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": "job_tracker"
}

try:
    engine = mysql.connector.connect(**config)
except Exception:
    raise Exception("Failed to connect to database")

app = Flask(__name__)

if __name__ == '__main__':
    app.run()