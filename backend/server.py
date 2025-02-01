from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/syncorsink"
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# MongoDB setup
client = MongoClient(app.config["MONGO_URI"])
db = client.syncorsink

@app.route("/api/data", methods=["GET"])
def get_data():
    # Example response
    data = {"message": "Hello from the backend!"}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
