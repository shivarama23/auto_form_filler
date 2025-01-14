import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from prompts import get_entities_prompt, get_chat_prompt_template
load_dotenv()

# Initialize the model
model = ChatOpenAI(
    openai_api_base=os.environ["OPENAI_BASE"],
    openai_api_key=f'{os.environ["LLMFOUNDRY_TOKEN"]}:{os.environ["PROJECT_NAME"]}',
    model="gpt-4o-mini"
)

# Define the prompt template
# prompt_template = ChatPromptTemplate.from_template("You are a helpful assistant. Always reply in 1 sentence as you are a chat assistant {history} User: {input}")
prompt_template = get_chat_prompt_template()

def get_response(user_input, session, user_role=""):
    # Initialize session keys if they don't exist
    session.setdefault("history", [])
    session.setdefault("user_data", {
        "name": "", "age": "", "email": "",
        "grade": "", "accommodations": "",
        "career": "", "interests": "", "strengths": "",
        "subjects": "", "enrollmentDate": "",
        "specialServices": "", "improvement": "", "budget": ""
    })
    session.setdefault("user_role", "")
    
    # Append the user's message to the session history
    session["history"].append({"role": "user", "content": user_input})
    if user_role and session["user_role"] == "":
        session["user_role"] = user_role
    else:
        pass
    
    # Prepare the prompt with history
    history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in session["history"]])
    prompt = prompt_template.invoke({"history": history, "input": user_input})
    
    # Get model response
    ai_response = model.invoke(prompt)
    ai_chat_output = ai_response.content
    if ai_chat_output.startswith("ai:"):
        ai_chat_output = ai_chat_output.replace("ai:", "").strip()
    session["history"].append({"role": "ai", "content": ai_chat_output})

    
    prompt_entity = get_entities_prompt(user_input)
    ai_response_entity = model.invoke(prompt_entity)
    output_entity = ai_response_entity.content

    try:
        output_dict = output_entity.replace('```json', '').replace('```', '').strip()
        output_json = json.loads(output_dict)
        for key, value in output_json.items():
            if key in session["user_data"]:
                if session["user_data"][key] == "":
                    session["user_data"][key] = value
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    
    return ai_chat_output, session
