from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from config import Config
from auth import auth_bp
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for frontend-backend communication
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Register authentication blueprint
app.register_blueprint(auth_bp)

# Initialize MongoDB client
client = MongoClient(app.config["MONGO_URI"])
db = client[os.getenv("MONGO_DB_NAME", "syncorsink")]  # Use database name from .env

@app.route("/")
def home():
    return jsonify({"message": "Connected to MongoDB successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
