import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
    const [message, setMessage] = useState(""); // Message from the backend
    const [user, setUser] = useState(null); // User data from the backend

    useEffect(() => {
        // Fetch user data to check if someone is logged in
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

        // Fetch a welcome message or connection message from the backend
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
        window.location.href = "http://127.0.0.1:5000/login";
    };

    const handleLogout = () => {
        fetch("http://127.0.0.1:5000/logout", {
            method: "POST",
            credentials: "include",
        })
            .then(() => {
                setUser(null);
                console.log("Logged out successfully");
            })
            .catch((error) => {
                console.error("Error logging out:", error);
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
                        <img
                            src={user.picture}
                            alt="User profile"
                            style={{ borderRadius: "50%", width: "100px", height: "100px" }}
                        />
                        <p>Email: {user.email}</p>
                        <button onClick={handleLogout}>Logout</button>
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
