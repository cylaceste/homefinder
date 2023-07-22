import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import MapPage from './MapPage';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/map" element={<MapPage />} />
      </Routes>
    </Router>
  );
}

function Chat() {
  const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const submitMessage = async (e) => {
    e.preventDefault();
    setMessages([...messages, {user: userMessage}]);
    setIsLoading(true);

    const response = await fetch('http://localhost:5000/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify([...messages, {user: userMessage}]),
    });

    const data = await response.json();
    setMessages([...messages, {user: userMessage}, {agent: data.agent}]);
    setIsLoading(false);
    setUserMessage('');
  };

  return (
    <div className="App">
      <header className="App-header">
        {messages.map((message, index) => (
          <p key={index} className={message.user ? "user" : "agent"}>
            {message.user || message.agent}
          </p>
        ))}
        {isLoading && <div className="loader"></div>}
        <form onSubmit={submitMessage}>
          <input 
            type="text" 
            value={userMessage} 
            onChange={(e) => setUserMessage(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading}>Send</button>
        </form>
        <Link to="/map">Go to Map</Link>
      </header>
    </div>
  );
}

export default App;
