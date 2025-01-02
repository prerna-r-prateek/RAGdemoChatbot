// frontend/src/App.js
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [userInput, setUserInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleSend = async () => {
    if (!userInput.trim()) return;

    // Add user message to chat
    setChatHistory([...chatHistory, { sender: 'user', text: userInput }]);

    try {
      // Send user query to backend
      const response = await axios.post('/api/chat', { text: userInput });

      // Add assistant's response to chat
      const assistantMsg = response.data.assistant;
      setChatHistory((prev) => [...prev, { sender: 'assistant', text: assistantMsg }]);
    } catch (error) {
      console.error('Error calling /api/chat:', error);
      setChatHistory((prev) => [
        ...prev,
        { sender: 'assistant', text: 'Sorry, something went wrong.' }
      ]);
    }

    setUserInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div style={styles.container}>
      <h1>RAG Chatbot</h1>
      <div style={styles.chatContainer}>
        {chatHistory.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: msg.sender === 'user' ? '#e0f7fa' : '#f1f1f1'
            }}
          >
            <strong>{msg.sender === 'user' ? 'You' : 'Assistant'}: </strong>
            {msg.text}
          </div>
        ))}
      </div>
      <div style={styles.inputContainer}>
        <input
          style={styles.input}
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question..."
        />
        <button style={styles.button} onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

// Inline styles for simplicity
const styles = {
  container: {
    width: '600px',
    margin: '0 auto',
    fontFamily: 'Arial, sans-serif'
  },
  chatContainer: {
    border: '1px solid #ccc',
    padding: '10px',
    height: '400px',
    overflowY: 'auto',
    marginBottom: '10px'
  },
  message: {
    maxWidth: '70%',
    padding: '8px',
    margin: '5px',
    borderRadius: '5px'
  },
  inputContainer: {
    display: 'flex'
  },
  input: {
    flex: 1,
    padding: '8px',
    fontSize: '16px'
  },
  button: {
    padding: '8px 16px',
    fontSize: '16px',
    marginLeft: '8px',
    cursor: 'pointer'
  }
};

export default App;

