# Enrollment Chat Assistant

## Setup
1. Clone the repository

2. Install backend dependencies:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3. Host redis server using docker
4. Host postgres server using docker

5. Run FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
6. Open `localhost:8000` in a browser

## Usage
- Real-time chat enabled with WebSocket
- Session-based chat history is maintained using sessionStorage


How to check redis?
Assuming you are using a docker instance of redis service.
docker exec -it redis-server redis-cli
> GET <session_id>
> GET session:qwqw8q ---> this is a example

Using Docker-compose:

cd <repo-folder>
docker-compose up --build -d
