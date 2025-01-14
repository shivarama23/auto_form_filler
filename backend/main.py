import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from session_manager import SessionManager
from chat import get_response
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()
db_config = {
    "host": "postgres",
    "port": 5432,
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

session_manager = SessionManager(redis_host="redis", redis_port=6379, db_config=db_config)

frontend_path = Path(__file__).parent.parent / "frontend"

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    try:
        await websocket.accept()
        session = session_manager.get_session(session_id)

        while True:
            # Receive the user message and role (if provided)
            data = await websocket.receive_text()
            # Check if the data is JSON string
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                data = {"message": data}

            role = data.get('role', "")
            user_message = data.get('message')

            # Get the response from the chatbot (pass the role if needed)
            response, session = get_response(user_message, session, role)

            # Save the updated session back to Redis
            session_manager.save_session(session_id, session)

            # Send the AI's response back to the frontend
            await websocket.send_text(json.dumps({"response": response, "form_data": session["user_data"]}))
    except WebSocketDisconnect as e:
        logging.info(f"Client {session_id} disconnected. Code: {e.code}, Reason: {e.reason}")
        session_manager.transfer_to_db(session_id)
        session_manager.delete_session(session_id)
        logging.info(f"Session {session_id} cleaned up from Redis.")


@app.get("/")
async def serve_index():
    return FileResponse(frontend_path / "index.html")
