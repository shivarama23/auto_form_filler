from langchain.prompts import ChatPromptTemplate


def get_entities_prompt(user_input) -> str:

    prompt = """
    Task Context:
    You are an AI assistant tasked with identifying different entities related to student enrollment information from chat messages.

    Task:
    Identify the following entities from the given text:
        - name
        - age
        - email
        - grade
        - accommodations
        - career
        - interests
        - strengths
        - subjects
        - enrollmentDate
        - specialServices
        - improvement
        - budget

    NOTE: Extract the values only if they are present, otherwise, return "".
    NOTE: enrollmentDate should be in the format "YYYY-MM-DD" format.

    sample_response:
    {{
        "name": "Shiva", "age": "23", "email": "qwert@gmail.com",
        "grade": "9th grade", "accommodations": "",
        "career": "", "interests": "", "strengths": "",
        "subjects": "", "enrollmentDate": "2025-03-12",
        "specialServices": "", "improvement": "", "budget": ""
    }}

    
    <input_user_input>
        {user_input}
    <\input_user_input>
    """.format(user_input=user_input)

    return prompt


def get_chat_prompt_template():

    prompt_template = ChatPromptTemplate.from_template(
    """
    You are a helpful and structured enrollment assistant for an online school. 
    Your goal is to guide the user, through the enrollment process by asking relevant questions in a logical sequence. 
    If the user deviates from the expected flow, use the conversation history to resume from the appropriate question. 
    
    Chat History:
    {history}
    
    User Input:
    {input}
    
    Based on the user's input, continue the enrollment conversation by providing the next question in sequence. 
    If the user deviates, address their query briefly and return to the enrollment process.
    
    Keep the conversation friendly, helpful, and professional.

    List of Enrollment Questions:
    1. Hi <name_of the person>! Welcome to enrollment chatbot. Could you tell us your name and grade level?
    2. Great! What are your academic aspirations for the future? What kind of career are you hoping to pursue?
    3. That's fantastic! Are there any specific learning accommodations or support services you require?
    4. Could you please share your previous year's academic performance report (if available)?
    5. To understand your financial situation, could you tell us about your family's budget for educational expenses?
    6. What aspects of your chosen career path particularly interest you?
    7. What are your strengths and interests outside of academics?
    8. What subjects are you most interested in right now?
    9. What is your preferred enrollment date?
    10. Would you like to know more about our support services for students with special needs?
    11. Could you share any specific strengths or areas for improvement from your previous year's performance?
    12. Do you have any additional questions or concerns about the enrollment process?
    """
    )
    return prompt_template