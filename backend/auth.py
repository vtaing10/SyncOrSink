import os
import logging
from authlib.integrations.flask_client import OAuth
from flask import Blueprint, jsonify, redirect, url_for, session, current_app

# Configure logging
logging.basicConfig(level=logging.DEBUG)

auth_bp = Blueprint("auth", __name__)

# Initialize OAuth
oauth = OAuth()

@auth_bp.before_app_request
def init_oauth():
    # Ensure OAuth is initialized with the current app
    oauth.init_app(current_app)

# Register the Google OAuth client
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
    'scope': 'openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/calendar.readonly',
},

)

@auth_bp.route("/login")
def login():
    logging.debug("Login endpoint hit.")
    redirect_uri = url_for("auth.auth_callback", _external=True)
    logging.debug(f"Redirect URI: {redirect_uri}")
    return google.authorize_redirect(redirect_uri)

@auth_bp.route("/logout", methods=["POST"])
def logout():
    logging.debug("Logout endpoint hit.")
    session.clear()  # Clear the session
    logging.debug("User session cleared.")
    return jsonify({"message": "Logged out successfully"}), 200



@auth_bp.route("/auth/callback")
def auth_callback():
    token = google.authorize_access_token()
    session["token"] = token  # Save token in session
    user_info = google.get("https://www.googleapis.com/oauth2/v3/userinfo").json()
    session["user"] = user_info  # Save user info in session
    return redirect(f"http://localhost:3000?email={user_info['email']}&name={user_info['name']}")

@auth_bp.route("/user")
def get_user():
    user = session.get("user")
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "No user is logged in"}), 401

