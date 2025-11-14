import { useEffect, useRef } from 'react'

function ChatMessage({ message, isUser, isEditing, editedText, onEditChange, onEdit, onApprove, onCancelEdit, threadId }) {
    const textareaRef = useRef(null)

    useEffect(() => {
        if (isEditing && textareaRef.current) {
            // Auto-resize textarea to fit content when entering edit mode
            textareaRef.current.style.height = 'auto'
            textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px'
        }
    }, [isEditing])

    return (
      <div style={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        margin: '10px 0',
        padding: '0 20px',
      }}>
        <div style={{
          maxWidth: isEditing ? '95%' : '70%',
          width: isEditing ? '95%' : 'auto',
          padding: isEditing ? '20px' : '12px 16px',
          borderRadius: '16px',
          backgroundColor: isUser ? '#007bff' : '#e9ecef',
          color: isUser ? '#fff' : '#333',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          wordWrap: 'break-word',
        }}>
          {isEditing ? (
            <div>
              <textarea
                ref={textareaRef}
                value={editedText}
                onChange={(e) => {
                  onEditChange(e.target.value)
                  // Auto-resize textarea to fit content
                  e.target.style.height = 'auto'
                  e.target.style.height = e.target.scrollHeight + 'px'
                }}
                style={{
                  width: '100%',
                  minHeight: '500px',
                  padding: '20px',
                  border: '2px solid #007bff',
                  borderRadius: '12px',
                  fontSize: '18px',
                  fontFamily: 'inherit',
                  lineHeight: '1.6',
                  resize: 'vertical',
                  outline: 'none',
                  boxSizing: 'border-box',
                  backgroundColor: '#fff',
                }}
              />
              <div style={{
                display: 'flex',
                gap: '8px',
                marginTop: '8px',
              }}>
                <button
                  onClick={onApprove}
                  style={{
                    padding: '6px 16px',
                    backgroundColor: '#28a745',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '500',
                  }}
                >
                  Approve
                </button>
                <button
                  onClick={onCancelEdit}
                  style={{
                    padding: '6px 16px',
                    backgroundColor: '#6c757d',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '500',
                  }}
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div>
              <div style={{ whiteSpace: 'pre-wrap' }}>{message}</div>
              {!isUser && threadId && (
                <div style={{
                  display: 'flex',
                  gap: '8px',
                  marginTop: '8px',
                }}>
                  <button
                    onClick={onEdit}
                    style={{
                      padding: '6px 16px',
                      backgroundColor: '#ffc107',
                      color: '#333',
                      border: 'none',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      fontSize: '14px',
                      fontWeight: '500',
                    }}
                  >
                    Edit
                  </button>
                  <button
                    onClick={onApprove}
                    style={{
                      padding: '6px 16px',
                      backgroundColor: '#28a745',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      fontSize: '14px',
                      fontWeight: '500',
                    }}
                  >
                    Approve
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    )
  }
  
  export default ChatMessage