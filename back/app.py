from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "allow_headers": "*",
        "methods": "*",
        "credentials": True
    }
})

@app.route("/", methods=["GET"])
def read_root():
    return jsonify({"message": "Hello World"})

@app.route("/ping/", methods=["GET"])
def read_ping():
    return jsonify({"message": "Pong"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
