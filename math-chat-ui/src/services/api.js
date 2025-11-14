const API_BASE_URL = 'http://127.0.0.1:8000' // Your backend URL

/**
 * Sends a math question to the agent API
 * @param {string} question - User's math question
 * @returns {Promise<{answer: string, threadId: string}>} - Response with answer and thread ID
 */
export const sendMessage = async (question) => {
  try {
    if (!question || !question.trim()) {
      throw new Error('Please enter a question')
    }

    // Call the /agent/start endpoint
    const response = await fetch(`${API_BASE_URL}/agent/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
      body: JSON.stringify({
        question: question.trim()
      }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(
        errorData.detail || `Failed to get response: ${response.status}`
      )
    }

    const data = await response.json()
    
    // The API returns { "thread_id": "...", "generated_answer": "..." }
    return {
      answer: data.generated_answer || 'No answer received',
      threadId: data.thread_id
    }
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
}

/**
 * Resumes an agent run with edited/approved answer
 * @param {string} threadId - Thread ID from the initial request
 * @param {string} finalAnswer - The edited/approved final answer
 * @returns {Promise<{status: string, message: string}>} - Response with status
 */
export const resumeAgent = async (threadId, finalAnswer) => {
  try {
    if (!threadId || !finalAnswer || !finalAnswer.trim()) {
      throw new Error('Thread ID and final answer are required')
    }

    // Call the /agent/resume endpoint
    const response = await fetch(`${API_BASE_URL}/agent/resume`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
      body: JSON.stringify({
        thread_id: threadId,
        final_answer: finalAnswer.trim()
      }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(
        errorData.detail || `Failed to resume agent: ${response.status}`
      )
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Resume API Error:', error)
    throw error
  }
}