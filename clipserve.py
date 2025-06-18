from flask import Flask, request, render_template_string, jsonify
import pyperclip
from datetime import datetime
import threading
import time
from cryptography.fernet import Fernet

# Temporary session key
fernet = Fernet(Fernet.generate_key())

# Start flask
app = Flask(__name__)

clipboard_history = []
last_clipboard = None

# HTML interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>📋 clipserve history</title>
    <style>
        body { font-family: monospace; background: #111; color: #0f0; padding: 2rem; }
        h1 { color: #0f0; }
        ul { list-style: none; padding: 0; }
        li { border-bottom: 1px solid #333; padding: 1em 0; }
        time { color: #888; font-size: 0.8em; }
        pre { white-space: pre-wrap; word-wrap: break-word; }
    </style>
    <script>
        function fetchHistory() {
            fetch('/history')
                .then(response => response.json())
                .then(data => {
                    const historyContainer = document.getElementById('history-container');
                    historyContainer.innerHTML = '';
                    data.history.reverse().forEach(item => {
                        const listItem = document.createElement('li');
                        listItem.innerHTML = `<time>${item.timestamp}</time><br><pre>${item.content}</pre>`;
                        historyContainer.appendChild(listItem);
                    });
                })
                .catch(error => console.error('Error fetching clipboard history:', error));
        }

        setInterval(fetchHistory, 2000);
    </script>
</head>
<body>
    <h1>📋 Clipboard History</h1>
    <ul id="history-container">
    </ul>
</body>
</html>
"""

# Flask rutes
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/push", methods=["POST"])
def push():
    content = request.form.get("content")
    if content:
        add_clipboard_item(content)
        return "Saved", 200
    return "Missing content", 400

@app.route("/history")
def history():
    return jsonify({
        "history": [
            {
                "content": fernet.decrypt(item["content"]).decode(),
                "timestamp": item["timestamp"]
            } for item in clipboard_history
        ]
    })

# Internal functions
def add_clipboard_item(content):
    if clipboard_history:
        decrypted_last = fernet.decrypt(clipboard_history[-1]["content"]).decode()
        if decrypted_last == content:
            return
    encrypted = fernet.encrypt(content.encode())
    clipboard_history.append({
        "content": encrypted,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def watch_clipboard():
    global last_clipboard
    while True:
        try:
            current = pyperclip.paste()
            if current and current != last_clipboard:
                last_clipboard = current
                add_clipboard_item(current)
        except Exception as e:
            print("Clipboard error:", e)
        time.sleep(1)

# Main execution
if __name__ == "__main__":
    print("[+] Session key generated (non-persistent). All history will be lost upon closing.")
    threading.Thread(target=watch_clipboard, daemon=True).start()
    app.run(host="0.0.0.0", port=6969)

