import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Initialize the model
model = ChatOpenAI(
    openai_api_base=os.environ["OPENAI_BASE"],
    openai_api_key=f'{os.environ["LLMFOUNDRY_TOKEN"]}:{os.environ["PROJECT_NAME"]}',
    model="gpt-4o-mini"
)

# Define the prompt template
prompt_template = ChatPromptTemplate.from_template("You are a helpful assistant. {history} User: {input}")

def get_response(user_input, session):
    # Initialize session keys if they don't exist
    session.setdefault("history", [])
    session.setdefault("user_data", {"name": "", "age": "", "email": ""})
    
    # Append the user's message to the session history
    session["history"].append({"role": "user", "content": user_input})
    
    # Prepare the prompt with history
    history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in session["history"]])
    prompt = prompt_template.invoke({"history": history, "input": user_input})
    
    # Get model response
    ai_response = model.invoke(prompt)
    session["history"].append({"role": "ai", "content": ai_response.content})
    
    # Extract form fields from conversation (case-insensitive parsing)
    user_input_lower = user_input.lower()
    if "name is" in user_input_lower:
        session["user_data"]["name"] = user_input.split("name is")[-1].strip()
    if "age is" in user_input_lower:
        session["user_data"]["age"] = user_input.split("age is")[-1].strip()
    if "email is" in user_input_lower:
        session["user_data"]["email"] = user_input.split("email is")[-1].strip()
    
    return ai_response.content, session
