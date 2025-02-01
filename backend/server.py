from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from configAPIURL import Config
from auth import auth_bp
from authlib.integrations.flask_client import OAuth

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize OAuth with Flask app
oauth = OAuth(app)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Register authentication blueprint
app.register_blueprint(auth_bp)

# Initialize MongoDB client
client = MongoClient(app.config["MONGO_URI"])
db = client[os.getenv("MONGO_DB_NAME", "syncorsink")]

@app.route("/")
def home():
    return jsonify({"message": "Connected to MongoDB successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
