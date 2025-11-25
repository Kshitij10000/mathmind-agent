import { useEffect, useRef } from 'react'
import './ChatMessage.css'

function ChatMessage({ message, isUser, isEditing, editedText, onEditChange, onEdit, onApprove, onCancelEdit, threadId }) {
    const textareaRef = useRef(null)

    useEffect(() => {
        if (isEditing && textareaRef.current) {
            // Auto-resize textarea to fit content when entering edit mode
            textareaRef.current.style.height = 'auto'
            textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px'
        }
    }, [isEditing])

    const containerClasses = `chat-message-container ${isUser ? 'user' : 'ai'}`
    const messageClasses = `chat-message ${isUser ? 'user' : 'ai'}`

    return (
        <div className={containerClasses}>
            <div className={isEditing ? 'editing-container' : messageClasses}>
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
                            className="editing-textarea"
                        />
                        <div className="message-actions">
                            <button
                                onClick={onApprove}
                                className="message-button approve-button"
                            >
                                Approve
                            </button>
                            <button
                                onClick={onCancelEdit}
                                className="message-button cancel-button"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                ) : (
                    <div>
                        <div>{message}</div>
                        {!isUser && threadId && (
                            <div className="message-actions">
                                <button
                                    onClick={onEdit}
                                    className="message-button edit-button"
                                >
                                    Edit
                                </button>
                                <button
                                    onClick={onApprove}
                                    className="message-button approve-button"
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