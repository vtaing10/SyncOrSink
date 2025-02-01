import os
from authlib.integrations.flask_client import OAuth
from flask import Blueprint, jsonify, redirect, url_for, session
from server import db

auth_bp = Blueprint("auth", __name__)

# Initialize OAuth
oauth = OAuth()

# Register the Google OAuth client
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v3/',
    client_kwargs={
        'scope': 'openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
    },
)

@auth_bp.route("/login")
def login():
    redirect_uri = url_for("auth.auth_callback", _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("http://localhost:3000")


@auth_bp.route("/auth/callback")
def auth_callback():
    token = google.authorize_access_token()
    user_info = google.get("userinfo").json()  # Fetch user info from Google
    session["user"] = user_info

    # Save user to MongoDB
    db.users.update_one(
        {"email": user_info["email"]},
        {"$set": user_info},
        upsert=True,
    )
    return redirect(f"http://localhost:3000?email={user_info['email']}&name={user_info['name']}")


@auth_bp.route("/user")
def get_user():
    user = session.get("user")
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "No user is logged in"}), 401
