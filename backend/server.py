from flask import Flask, jsonify, redirect, url_for, session
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from auth import auth_bp
from authlib.integrations.flask_client import OAuth
from GoogleCal import calendar_bp

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_default_secret_key")  # Ensure SECRET_KEY is set

# Enable CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Register the auth blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(calendar_bp)

# Initialize OAuth
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
    },
)

# Initialize MongoDB client
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB_NAME", "syncorsink")]

# Routes
@app.route("/")
def home():
    return jsonify({"message": "Connected to the backend successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
