# backend\math_agent\llm\services.py
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    "gemini-2.5-flash-lite",
    temperature=0
)

def generate_solution(question: str, context: str) -> str:
    """Generates the final answer based on question and context"""

    prompt = f"""You are a math professor. Your goal is to help a student.
    Use the following CONTEXT to answer the student's QUESTION.
    Generate a clear, step-by-step solution. If the context is not relevant,
    say you could not find a good answer.
    Dont greet the student , be like a actual professor who is good and
    has teacher like attitude.
    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:"""
    
    try:
        response = llm.invoke(prompt)
        answer = response.content.strip()
        return answer
    
    except Exception as e:
        print(f"Error during solution generation: {e}")
        return "I'm sorry, I couldn't generate an answer at this time."
    
if __name__ == '__main__':

    question = "Solve for (x) in the equation (2(x+3)=10)"
    context = ""  # Add appropriate context here
    is_valid = generate_solution(question, context)
    print(is_valid)