import { useState } from 'react'
import ChatMessage from '../components/ChatMessage'
import ChatInput from '../components/ChatInput'
import { sendMessage, resumeAgent } from '../services/api'
import './MathChat.css'

function MathChat() {
  const [messages, setMessages] = useState([
    { text: 'Hello! I\'m your math assistant. Ask me any math question and I\'ll help you solve it.', isUser: false, threadId: null }
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [editingIndex, setEditingIndex] = useState(null)
  const [editedText, setEditedText] = useState('')

  const handleSendMessage = async (text) => {
    // Add user message
    const userMessage = { text, isUser: true, threadId: null }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Call your backend API
      const response = await sendMessage(text)
      
      // Add AI response with thread ID
      const aiMessage = { 
        text: response.answer, 
        isUser: false,
        threadId: response.threadId 
      }
      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      const errorMessage = { 
        text: error.message || 'Sorry, I couldn\'t connect to the server. Please check if your backend is running.', 
        isUser: false,
        threadId: null
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleEdit = (index) => {
    setEditingIndex(index)
    setEditedText(messages[index].text)
  }

  const handleCancelEdit = () => {
    setEditingIndex(null)
    setEditedText('')
  }

  const handleApprove = async (index) => {
    const message = messages[index]
    const finalAnswer = editingIndex === index ? editedText : message.text
    
    if (!message.threadId) {
      // No thread ID, just update the message if editing
      if (editingIndex === index) {
        setMessages(prev => prev.map((msg, i) => 
          i === index ? { ...msg, text: editedText } : msg
        ))
        setEditingIndex(null)
        setEditedText('')
      }
      return
    }

    setIsLoading(true)
    try {
      // Call the resume API
      await resumeAgent(message.threadId, finalAnswer)
      
      // Update the message if it was edited
      if (editingIndex === index) {
        setMessages(prev => prev.map((msg, i) => 
          i === index ? { ...msg, text: editedText } : msg
        ))
      }
      
      setEditingIndex(null)
      setEditedText('')
      
      // Show success message
      const successMessage = { 
        text: '✓ Answer approved and feedback sent to agent!', 
        isUser: false,
        threadId: null
      }
      setMessages(prev => [...prev, successMessage])
    } catch (error) {
      const errorMessage = { 
        text: `Error: ${error.message || 'Failed to send feedback'}`, 
        isUser: false,
        threadId: null
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="math-chat">
      {/* Messages area */}
      <div className="messages-area">
        {messages.map((msg, index) => (
          <ChatMessage 
            key={index} 
            message={msg.text} 
            isUser={msg.isUser}
            isEditing={editingIndex === index}
            editedText={editedText}
            onEditChange={setEditedText}
            onEdit={() => handleEdit(index)}
            onApprove={() => handleApprove(index)}
            onCancelEdit={handleCancelEdit}
            threadId={msg.threadId}
          />
        ))}
        {isLoading && (
          <ChatMessage 
            message="Thinking..." 
            isUser={false}
            threadId={null}
          />
        )}
      </div>

      {/* Input area */}
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  )
}

export default MathChat