from flask import Flask
from crud import engine

app = Flask(__name__)

if __name__ == '__main__':
    app.run()
    engine.close()