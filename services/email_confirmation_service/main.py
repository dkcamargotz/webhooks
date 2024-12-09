from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='127.0.0.1',
        port='5001'
    )
