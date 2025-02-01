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
    access_token_url="https://accounts.google.com/o/oauth2/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
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
    return jsonify({"message": "Connected to MongoDB successfully!"})

@app.route("/login")
def login():
    """
    Redirects the user to Google's OAuth 2.0 consent screen.
    """
    redirect_uri = url_for("auth_callback", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/auth/callback")
def auth_callback():
    """
    Handles the OAuth callback after the user authenticates with Google.
    """
    token = google.authorize_access_token()
    user_info = google.get("userinfo").json()
    # Save user info in session
    session["user"] = user_info
    return jsonify(user_info)  # Replace with a redirect to your frontend if needed

@app.route("/logout")
def logout():
    """
    Logs the user out and clears the session.
    """
    session.pop("user", None)
    return redirect("/")

@app.route("/profile")
def profile():
    """
    Displays the profile of the currently logged-in user.
    """
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    return jsonify(user)

if __name__ == "__main__":
    app.run(debug=True)
