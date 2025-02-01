from flask import Blueprint, redirect, url_for
from authlib.integrations.flask_client import OAuth
import os

auth_bp = Blueprint("auth", __name__)

oauth = OAuth()

oauth.register(
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

@auth_bp.route("/login")
def login():
    redirect_uri = url_for("auth.callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route("/auth/callback")
def callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.get("userinfo").json()
    return user_info
