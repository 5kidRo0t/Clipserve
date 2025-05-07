from flask import Flask, request, render_template_string, jsonify
import pyperclip
from datetime import datetime
import threading
import time

app = Flask(__name__)

clipboard_history = []
last_clipboard = None  # Tracks last copied item

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
    </style>
    <script>
        // Function to fetch clipboard history from the server and update the list
        function fetchHistory() {
            fetch('/history')
                .then(response => response.json())
                .then(data => {
                    const historyContainer = document.getElementById('history-container');
                    historyContainer.innerHTML = '';  // Clear current list
                    data.history.reverse().forEach(item => {
                        const listItem = document.createElement('li');
                        listItem.innerHTML = `<time>${item.timestamp}</time><br><pre>${item.content}</pre>`;
                        historyContainer.appendChild(listItem);
                    });
                })
                .catch(error => console.error('Error fetching clipboard history:', error));
        }

        // Fetch history every 2 seconds
        setInterval(fetchHistory, 2000);
    </script>
</head>
<body>
    <h1>📋 Clipboard History</h1>
    <ul id="history-container">
        <!-- Clipboard history will appear here -->
    </ul>
</body>
</html>
"""

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
    return jsonify({"history": clipboard_history})

def add_clipboard_item(content):
    if clipboard_history and clipboard_history[-1]["content"] == content:
        return  # Don't re-add duplicate
    clipboard_history.append({
        "content": content,
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

if __name__ == "__main__":
    # Start background thread to monitor clipboard
    threading.Thread(target=watch_clipboard, daemon=True).start()
    app.run(host="0.0.0.0", port=6969)
