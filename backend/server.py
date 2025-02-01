from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for frontend-backend communication
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Initialize MongoDB client
client = MongoClient(app.config["MONGO_URI"])
db = client.your_database_name  # Replace with your database name

@app.route("/")
def home():
    return jsonify({"message": "Connected to MongoDB successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
