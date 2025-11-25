import { useState } from 'react'
import './ChatInput.css'

function ChatInput({ onSendMessage }) {
    const [input, setInput] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()
        if (input.trim()) {
            onSendMessage(input.trim())
            setInput('');
        }
    }

    return (
        <form onSubmit={handleSubmit} className="chat-input-form">
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a math question..."
                className="chat-input"
            />
            <button
                type="submit"
                className="send-button"
            >
                Send
            </button>
        </form>
    )
}

export default ChatInput