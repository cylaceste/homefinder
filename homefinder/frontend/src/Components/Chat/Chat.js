import React, { useState } from 'react';
import './Chat.css';

function Chat() {
    const [messages, setMessages] = useState([]);
    const [userMessage, setUserMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const submitMessage = async (e) => {
        e.preventDefault();
        const newMessage = {role: "user", content: userMessage};

        // To make sure that state update has the most recent state, 
        // use a function within setMessages
        setMessages(prevMessages => [...prevMessages, newMessage]);
        setIsLoading(true);

        const response = await fetch('http://localhost:5000/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify([...messages, newMessage]),
        });

        const data = await response.json();
        setMessages(data.message_history);
        setIsLoading(false);
        setUserMessage('');
    };

    return (
        <div className="Chat">
            <header className="Chat-header">
                {messages.map((message, index) => (
                    <p key={index} className={message.role === 'user' ? "user" : "agent"}>
                        {message.content}
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
            </header>
        </div>
    );
}

export default Chat;
