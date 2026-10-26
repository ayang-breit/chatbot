INDEX = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dropbox AI Assistant</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 100%; max-width: 800px; background: #fff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: flex; flex-direction: column; height: 85vh; overflow: hidden; }
        .chat-header { background: #2563eb; color: white; padding: 20px; text-align: center; }
        .chat-header h2 { margin: 0; font-size: 1.2rem; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .message { padding: 12px 16px; border-radius: 8px; max-width: 80%; line-height: 1.5; white-space: pre-wrap; }
        .user-message { background: #2563eb; color: white; align-self: flex-end; border-bottom-right-radius: 0; }
        .bot-message { background: #f1f5f9; color: #1e293b; align-self: flex-start; border-bottom-left-radius: 0; }
        .input-area { display: flex; padding: 20px; background: #fff; border-top: 1px solid #e2e8f0; }
        input[type="text"] { flex: 1; padding: 12px; border: 1px solid #cbd5e1; border-radius: 6px; margin-right: 12px; font-size: 1rem; outline: none; }
        input[type="text"]:focus { border-color: #2563eb; }
        button { padding: 12px 24px; background: #2563eb; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; font-weight: bold; transition: background 0.2s; }
        button:hover { background: #1d4ed8; }
        .loading { align-self: flex-start; color: #64748b; font-style: italic; font-size: 0.9rem; display: none; margin-left: 10px; }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">
        <h2>Dropbox File Assistant</h2>
    </div>
    <div class="chat-messages" id="chat-messages">
        <div class="message bot-message">Hello! I am connected to your Dropbox. You can ask me to list folders or read files for you.</div>
        <div class="loading" id="loading">Agent is thinking and searching...</div>
    </div>
    <div class="input-area">
        <input type="text" id="user-input" placeholder="Ask about a file in your Dropbox..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">Send</button>
    </div>
</div>

<script>
    async function sendMessage() {
        const inputField = document.getElementById('user-input');
        const message = inputField.value.trim();
        if (!message) return;

        // Display user message
        appendMessage(message, 'user-message');
        inputField.value = '';

        // Show loading text
        const loading = document.getElementById('loading');
        loading.style.display = 'block';

        try {
            // Send request to your Flask /chat endpoint
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            if (data.response) {
                appendMessage(data.response, 'bot-message');
            } else if (data.error) {
                appendMessage("Error: " + data.error, 'bot-message');
            }
        } catch (error) {
            appendMessage("Network Error: Failed to connect to the backend server.", 'bot-message');
        } finally {
            loading.style.display = 'none';
        }
    }

    function appendMessage(text, className) {
        const chatMessages = document.getElementById('chat-messages');
        const loadingNode = document.getElementById('loading');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message ' + className;
        messageDiv.textContent = text;
        
        // Insert the new message right before the hidden "loading" text
        chatMessages.insertBefore(messageDiv, loadingNode);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to bottom
    }

    function handleKeyPress(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    }
</script>
</body>
</html>
'''