from flask import Blueprint, jsonify, session
from authlib.integrations.flask_client import OAuth
import requests

calendar_bp = Blueprint("calendar", __name__)

@calendar_bp.route("/events", methods=["GET"])
def fetch_calendar_events():
    # Ensure the user is logged in
    user = session.get("user")
    if not user:
        return jsonify({"error": "User not logged in"}), 401

    # Get the access token
    token = session.get("token")
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    # Fetch events from Google Calendar API
    headers = {"Authorization": f"Bearer {token['access_token']}"}
    response = requests.get(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events", headers=headers
    )

    if response.status_code == 200:
        events = response.json()
        return jsonify(events)
    else:
        return jsonify({"error": "Failed to fetch events", "details": response.json()}), response.status_code
