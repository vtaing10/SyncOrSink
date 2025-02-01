from flask import Flask, jsonify, redirect, url_for, session
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from configAPIURL import Config
from authlib.integrations.flask_client import OAuth

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]  # Ensure SECRET_KEY is set

# Initialize OAuth with Flask app
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Initialize MongoDB client
client = MongoClient(app.config["MONGO_URI"])
db = client[os.getenv("MONGO_DB_NAME", "syncorsink")]

# Routes
@app.route("/")
def home():
    return jsonify({"message": "Connected to MongoDB successfully! AND WELCOME TO SYNCORSINK"})

@app.route("/login")
def login():
    redirect_uri = url_for("auth_callback", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/auth/callback")
def auth_callback():
    token = google.authorize_access_token()  # Get the access token
    user_info = google.get("https://www.googleapis.com/oauth2/v3/userinfo").json()  # Fetch user info from Google
    session["user"] = user_info  # Save user info in the session
    return jsonify(user_info)  # Optionally redirect to your frontend

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    return jsonify(user)

if __name__ == "__main__":
    app.run(debug=True)
