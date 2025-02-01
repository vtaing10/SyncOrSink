from flask import Blueprint, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

auth_bp = Blueprint("auth", __name__)

# Set up OAuth
oauth = OAuth()
oauth.init_app(auth_bp)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid email profile"},
)

@auth_bp.route("/login")
def login():
    return google.authorize_redirect(url_for("auth.authorize", _external=True))

@auth_bp.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    session["user"] = token
    return redirect(url_for("home"))
