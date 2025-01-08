// Ensure each window/tab has its own session ID
const sessionId = sessionStorage.getItem('session_id') || generateSessionId();
sessionStorage.setItem('session_id', sessionId);

// Initialize the WebSocket with the session ID
const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);

let selectedRole = null;  // Store the selected role temporarily

ws.onmessage = (event) => {
    const chatContainer = document.getElementById('chat-container');
    const msg = document.createElement('div');
    const data = JSON.parse(event.data);
    msg.textContent = `AI: ${data.response}`;
    msg.classList.add('chat-message', 'ai');
    chatContainer.appendChild(msg);

    // Auto-fill form fields
    // if (data.form_data.name) {
    //     document.getElementById("name").value = data.form_data.name;
    // }
    // if (data.form_data.age) {
    //     document.getElementById("age").value = data.form_data.age;
    // }
    // if (data.form_data.email) {
    //     document.getElementById("email").value = data.form_data.email;
    // }

    // Auto-fill form fields dynamically
    const formData = data.form_data || {};
    console.log(formData);
    Object.keys(formData).forEach(key => {
        const field = document.getElementById(key);
        if (field) {
            field.value = formData[key];
        }
    });
    
};

// Store the selected role when the user clicks on "Student" or "Parent"
function selectRole(role) {
    selectedRole = role;  // Save the role temporarily
    const chatContainer = document.getElementById('chat-container');
    const msg = document.createElement('div');
    msg.textContent = `You: ${role}`;
    msg.classList.add('chat-message', 'user');
    chatContainer.appendChild(msg);

    // Enable user input for the next message
    const userInputField = document.getElementById('userInput');
    userInputField.disabled = false;
    userInputField.placeholder = "Type a message...";
}

// Send the user's message along with the selected role
function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    const chatContainer = document.getElementById('chat-container');
    const msg = document.createElement('div');
    msg.textContent = `You: ${userInput}`;
    msg.classList.add('chat-message', 'user');
    chatContainer.appendChild(msg);

    // Only send the message and role if the role is selected
    if (selectedRole) {
        const messageToSend = {
            role: selectedRole,
            message: userInput
        };
        ws.send(JSON.stringify(messageToSend));  // Send both role and message
    } else {
        // If no role is selected, just send the message without a role
        ws.send(userInput);
    }

    document.getElementById('userInput').value = '';  // Clear the input field
    selectedRole = null;  // Clear the role after sending the message
}

function generateSessionId() {
    const sessionId = Math.random().toString(36).substring(7);
    sessionStorage.setItem('session_id', sessionId);
    return sessionId;
}

// Function to show the welcome message and role selection buttons
function showWelcomeMessage() {
    const chatContainer = document.getElementById('chat-container');
    const welcomeMsg = document.createElement('div');
    welcomeMsg.textContent = "AI: Hi, I'm your AI Assistant. Are you a parent or student?";
    welcomeMsg.classList.add('chat-message', 'ai');
    chatContainer.appendChild(welcomeMsg);

    const buttonContainer = document.createElement('div');
    buttonContainer.classList.add('flex', 'gap-4', 'mt-4');

    const studentButton = document.createElement('button');
    studentButton.textContent = 'Student';
    studentButton.classList.add('px-4', 'py-2', 'bg-blue-600', 'text-white', 'rounded');
    studentButton.onclick = () => selectRole('Student');

    const parentButton = document.createElement('button');
    parentButton.textContent = 'Parent';
    parentButton.classList.add('px-4', 'py-2', 'bg-green-600', 'text-white', 'rounded');
    parentButton.onclick = () => selectRole('Parent');

    buttonContainer.appendChild(studentButton);
    buttonContainer.appendChild(parentButton);
    chatContainer.appendChild(buttonContainer);
}

window.onload = () => {
    showWelcomeMessage();  // Show the welcome message on page load
    document.getElementById('userInput').disabled = true;
    document.getElementById('userInput').placeholder = "Select an option first...";
};
