const API_BASE_URL = 'http://127.0.0.1:8000' // Your backend URL


const extractNumber = (text) => {
  // Remove all non-digit characters and extract first number
  const numbers = text.match(/\d+/)
  if (numbers) {
    return parseInt(numbers[0], 10)
  }
  return null
}

/**
 * Sends a request to the /math endpoint to get multiplication table
 * @param {string} userInput - User's message (e.g., "2", "table of 5")
 * @returns {Promise<string>} - Formatted multiplication table as string
 */
export const sendMessage = async (userInput) => {
  try {
    // Extract number from user input
    const number = extractNumber(userInput)
    
    if (!number || number < 1) {
      throw new Error('Please enter a valid number (e.g., "2" or "table of 5")')
    }

    // Call the /math endpoint with number as query parameter
    const response = await fetch(`${API_BASE_URL}/math?number=${number}`, {
      method: 'POST',
      headers: {
        'accept': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`Failed to get multiplication table: ${response.status}`)
    }

    const data = await response.json()
    
    // The API returns { "message": ["2 x 1 = 2", "2 x 2 = 4", ...] }
    // Format it as a readable string
    if (data.message && Array.isArray(data.message)) {
      return `Multiplication table for ${number}:\n\n${data.message.join('\n')}`
    }
    
    return 'No response received'
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
}