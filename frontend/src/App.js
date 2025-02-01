import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
    const [message, setMessage] = useState("");

    useEffect(() => {
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
