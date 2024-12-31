// Ensure each window/tab has its own session ID
const sessionId = sessionStorage.getItem('session_id') || generateSessionId();
sessionStorage.setItem('session_id', sessionId);

// Initialize the WebSocket with the session ID
const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);

ws.onmessage = (event) => {
    const chatContainer = document.getElementById('chat-container');
    const msg = document.createElement('div');
    const data = JSON.parse(event.data);
    msg.textContent = `AI: ${data.response}`;
    msg.classList.add('chat-message', 'ai');
    chatContainer.appendChild(msg);

    // Auto-fill form fields
    if (data.form_data.name) {
        document.getElementById("name").value = data.form_data.name;
    }
    if (data.form_data.age) {
        document.getElementById("age").value = data.form_data.age;
    }
    if (data.form_data.email) {
        document.getElementById("email").value = data.form_data.email;
    }
};

function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    const chatContainer = document.getElementById('chat-container');
    const msg = document.createElement('div');
    msg.textContent = `You: ${userInput}`;
    msg.classList.add('chat-message', 'user');
    chatContainer.appendChild(msg);
    ws.send(userInput);
    document.getElementById('userInput').value = '';
}

function generateSessionId() {
    const sessionId = Math.random().toString(36).substring(7);
    sessionStorage.setItem('session_id', sessionId);
    return sessionId;
}
