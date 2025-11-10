import { useState } from 'react'

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
        <form onSubmit={handleSubmit} style={{
            display: 'flex',
            padding: '20px',
            backgroundColor: '#fff',
            borderTop: '1px solid #e0e0e0',
            gap: '10px',
        }}>
        <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a math question..."
            style={{
                flex: 1,
                padding: '12px 16px',
                border: '1px solid #ddd',
                borderRadius: '24px',
                fontSize: '16px',
                outline: 'none',
        }}
      />
      <button
        type="submit"
        style={{
          padding: '12px 24px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '24px',
          cursor: 'pointer',
          fontSize: '16px',
          fontWeight: '500',
        }}
      >
        Send
      </button>
    </form>
)
}

export default ChatInput