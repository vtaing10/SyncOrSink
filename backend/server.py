from flask import Flask, jsonify, redirect, url_for, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
from configAPIURL import Config
from authlib.integrations.flask_client import OAuth
from GoogleCal import calendar_bp
from auth import auth_bp

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")
  # Ensure SECRET_KEY is set

app.config.update(
    SESSION_COOKIE_SECURE=False,  # Set to True in production
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(calendar_bp)

# Initialize OAuth with Flask app
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile https://www.googleapis.com/auth/calendar.readonly",
    },
)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Routes
@app.route("/")
def home():
    return jsonify({"message": "Welcome to SyncOrSink!"})

@app.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        return jsonify({"error": "User not logged in"}), 401
    return jsonify(user)

@app.route("/login")
def login():
    redirect_uri = url_for("auth.auth_callback", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    session.pop("token", None)
    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
