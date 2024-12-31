# Enrollment Chat Assistant

## Setup
1. Clone the repository
2. Install backend dependencies:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```
3. Run FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
4. Open `frontend/index.html` in a browser

## Usage
- Real-time chat enabled with WebSocket
- Session-based chat history is maintained using sessionStorage