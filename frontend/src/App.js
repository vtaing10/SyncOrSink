import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
    const [message, setMessage] = useState("");

    useEffect(() => {
        // Fetch data from the backend
        fetch("http://localhost:5000/")
            .then((response) => response.json())
            .then((data) => {
                setMessage(data.message);
            })
            .catch((error) => {
                console.error("Error connecting to backend:", error);
                setMessage("Failed to connect to the backend.");
            });
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <h1>Welcome to SyncOrSink!</h1>
                <p>{message}</p>
            </header>
        </div>
    );
}

export default App;
