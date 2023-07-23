import React, { useState } from 'react';
import './Chat.css';

function Chat({ setProperties }) {
  const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const submitMessage = async (e) => {
    e.preventDefault();
    setMessages([...messages, {role: "user", content: userMessage}]);
    setIsLoading(true);

    const response = await fetch('http://localhost:5000/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify([...messages, {role: "user", content: userMessage}]),
    });

    const data = await response.json();
    console.log(data)
    setMessages(data.message_history);
    setProperties(data.properties);
    setIsLoading(false);
    setUserMessage('');
  };

  return (
    <div className="Chat">
      {messages.map((message, index) => (
        message.role === "user" ? 
        <p key={index} className="user-message">{message.content}</p> : 
        message.role === "assistant" ? 
        <p key={index} className="agent-message">{message.content}</p> : null
      ))}
      {isLoading && <div className="loader"></div>}
      <form onSubmit={submitMessage}>
        <input 
          type="text" 
          value={userMessage} 
          onChange={(e) => setUserMessage(e.target.value)}
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading} className="send-button">Send</button>
      </form>
    </div>
  );
}

export default Chat;
