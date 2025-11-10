import { useState } from 'react'
import ChatMessage from '../components/ChatMessage'
import ChatInput from '../components/ChatInput'
import { sendMessage } from '../services/api'

function MathChat() {
  const [messages, setMessages] = useState([
    { text: 'Hello! Insert a number to get table', isUser: false }
  ])
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async (text) => {
    // Add user message
    const userMessage = { text, isUser: true }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Call your backend API
      const response = await sendMessage(text)
      const aiMessage = { text: response, isUser: false }
      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      const errorMessage = { 
        text: error.message || 'Sorry, I couldn\'t connect to the server. Please check if your backend is running.', 
        isUser: false 
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      backgroundColor: '#f8f9fa',
    }}>
      {/* Messages area */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '20px 0',
      }}>
        {messages.map((msg, index) => (
          <ChatMessage 
            key={index} 
            message={msg.text} 
            isUser={msg.isUser} 
          />
        ))}
        {isLoading && (
          <ChatMessage 
            message="Thinking..." 
            isUser={false} 
          />
        )}
      </div>

      {/* Input area */}
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  )
}

export default MathChat