import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
    const [message, setMessage] = useState(""); // Message from the backend
    const [user, setUser] = useState(null); // User data
    const [events, setEvents] = useState([]); // Calendar events

    useEffect(() => {
        console.log("App mounted. Checking for query parameters.");
        const params = new URLSearchParams(window.location.search);
        const email = params.get("email");
        const name = params.get("name");

        if (email && name) {
            console.log("Query parameters found:", { email, name });
            setUser({ email, name });
            window.history.replaceState({}, document.title, "/");
        } else {
            console.log("No query parameters found. Fetching user from backend.");
            fetch("http://127.0.0.1:5000/user")
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error("User not logged in");
                })
                .then((userData) => {
                    console.log("User Data:", userData);
                    setUser(userData);
                })
                .catch((error) => {
                    console.error("Error fetching user data:", error);
                });
        }

        console.log("Fetching welcome message from backend.");
        fetch("http://127.0.0.1:5000/")
            .then((response) => response.json())
            .then((data) => {
                console.log("Backend response:", data);
                setMessage(data.message);
            })
            .catch((error) => {
                console.error("Error connecting to backend:", error);
                setMessage("Failed to connect to the backend.");
            });
    }, []);

    const handleLogin = () => {
        console.log("Login button clicked. Redirecting to login.");
        window.location.href = "http://127.0.0.1:5000/login";
    };

    const handleLogout = () => {
        fetch("http://127.0.0.1:5000/logout", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => {
                if (response.ok) {
                    setUser(null);
                    console.log("Logged out successfully");
                } else {
                    throw new Error("Logout failed");
                }
            })
            .catch((error) => {
                console.error("Error logging out:", error);
            });
    };

    const fetchEvents = () => {
        console.log("Fetching Google Calendar events...");
        fetch("http://127.0.0.1:5000/events", {
            method: "GET",
            credentials: "include",
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error("Failed to fetch events");
            })
            .then((data) => {
                console.log("Fetched events:", data);
                setEvents(data.items || []);
            })
            .catch((error) => {
                console.error("Error fetching events:", error);
            });
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Welcome to SyncOrSink!</h1>
                <p>{message}</p>
                {user ? (
                    <div>
                        <h2>Welcome, {user.name}!</h2>
                        <p>Email: {user.email}</p>
                        <button onClick={handleLogout}>Logout</button>
                        <button onClick={fetchEvents}>Fetch Google Calendar Events</button>
                        {events.length > 0 && (
                            <div>
                                <h3>Upcoming Events:</h3>
                                <ul>
                                    {events.map((event) => (
                                        <li key={event.id}>
                                            <strong>{event.summary}</strong> - {event.start?.dateTime || event.start?.date}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                ) : (
                    <div>
                        <p>Please log in to access your account.</p>
                        <button onClick={handleLogin}>Login</button>
                    </div>
                )}
            </header>
        </div>
    );
}

export default App;
