from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
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
session_manager = SessionManager()

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
        session = session_manager.get_session(session_id)  # Get or create the session
        
        while True:
            # Receive the user message
            data = await websocket.receive_text()
            
            # Get the response from the chatbot, along with any form data
            response, session = get_response(data, session)

            # Send the AI's response and form data back to the frontend
            await websocket.send_text(json.dumps({"response": response, "form_data": session["user_data"]}))
    except WebSocketDisconnect as e:
        # Handle the disconnect gracefully
        logging.info(f"Client {session_id} disconnected. Code: {e.code}, Reason: {e.reason}")
        # Optionally, remove the session or perform any other cleanup if necessary
        if session_id in session_manager.sessions:
            del session_manager.sessions[session_id]
        logging.info(f"Session {session_id} cleaned up.")


@app.get("/")
async def serve_index():
    return FileResponse(frontend_path / "index.html")