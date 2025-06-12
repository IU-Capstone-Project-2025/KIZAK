from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


@app.route("/")
def read_root():
    return jsonify({"message": "Hello World"})


@app.route("/ping")
def read_ping():
    return {"message": "Pong"}
