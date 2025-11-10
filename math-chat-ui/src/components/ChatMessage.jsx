function ChatMessage({ message, isUser }) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        margin: '10px 0',
        padding: '0 20px',
      }}>
        <div style={{
          maxWidth: '70%',
          padding: '12px 16px',
          borderRadius: '16px',
          backgroundColor: isUser ? '#007bff' : '#e9ecef',
          color: isUser ? '#fff' : '#333',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          wordWrap: 'break-word',
        }}>
          <div style={{ whiteSpace: 'pre-wrap' }}>{message}</div>
        </div>
      </div>
    )
  }
  
  export default ChatMessage