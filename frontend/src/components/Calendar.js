import React, { useEffect, useState } from "react";

function Calendar() {
    const [events, setEvents] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/calendar/events")
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error("Failed to fetch calendar events");
            })
            .then((data) => {
                console.log("Fetched Events:", data);
                setEvents(data.items || []); // `items` contains the event list
            })
            .catch((error) => {
                console.error("Error fetching calendar events:", error);
                setError(error.message);
            });
    }, []);

    return (
        <div>
            <h1>Google Calendar Events</h1>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <ul>
                {events.map((event) => (
                    <li key={event.id}>
                        <strong>{event.summary}</strong>
                        <p>{new Date(event.start.dateTime || event.start.date).toLocaleString()}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Calendar;
