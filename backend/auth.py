from flask import Blueprint, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

auth_bp = Blueprint("auth", __name__)

# Initialize OAuth
oauth = OAuth()

# Register Google OAuth client
google = oauth.register(
    "google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    client_kwargs={"scope": "openid email profile"},
)

@auth_bp.route("/login")
def login():
    return google.authorize_redirect(redirect_uri=url_for("auth.callback", _external=True))

@auth_bp.route("/callback")
def callback():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    session["user"] = user_info
    return redirect("/")  # Redirect to the home page

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
