from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client.syncorsink  # Database name

@app.route("/")
def home():
    return jsonify({"message": "Backend is working!"})

if __name__ == "__main__":
    app.run(debug=True)
