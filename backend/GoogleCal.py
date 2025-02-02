import logging
import requests
from flask import Blueprint, jsonify, session

calendar_bp = Blueprint("calendar", __name__)

@calendar_bp.route("/events", methods=["GET"])
def fetch_calendar_events():
    token = session.get("token")
    if not token:
        logging.error("Access token missing from session.")
        return jsonify({"error": "Missing access token"}), 401

    headers = {"Authorization": f"Bearer {token['access_token']}"}
    response = requests.get(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",
        headers=headers,
    )
    logging.debug(f"Google Calendar API response: {response.status_code} - {response.text}")

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        logging.error("Failed to fetch events")
        return jsonify({"error": "Failed to fetch events", "details": response.json()}), response.status_code
