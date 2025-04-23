from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Simple rule-based responses
responses = {
    "hours": "I need a 2 days advance order, what would you like!",
    "menu": "You can find all the details on my menu page: https://drive.google.com/file/d/1zW36ZS74NClwFcmEYEixZ5qoG_mSZcl8/view?usp=sharing! ",
    "prices": "What product's price are you looking for? You can find all pricing details on my menu page: https://drive.google.com/file/d/1zW36ZS74NClwFcmEYEixZ5qoG_mSZcl8/view?usp=sharing! ",
    "contact": "You can reach me at 949-466-4055. I accept Venmo or cash for payments.",
    "location": "You can pick up your order at 1330 East Sedona Drive, Orange, CA. I also deliver within a 5-mile radius, or farther for larger orders.",
    "default": "I’m not sure how to answer that. Can you ask something else?"
}

# HTML template for the chatbot interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Chatbot for Small Businesses</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f0f0f0; }
        #chatbox { border: 1px solid #ccc; width: 300px; height: 400px; overflow-y: scroll; padding: 10px; background-color: white; }
        #input { width: 300px; padding: 10px; margin-top: 10px; }
        #send { padding: 10px; margin-top: 5px; }
        .message { margin: 5px 0; }
        .user { text-align: right; color: blue; }
        .bot { text-align: left; color: green; }
    </style>
</head>
<body>
    <h1>AI Chatbot</h1>
    <div id="chatbox"></div>
    <input type="text" id="input" placeholder="Type your question..." onkeypress="if(event.keyCode==13) sendMessage()">
    <button id="send" onclick="sendMessage()">Send</button>
    <script>
        function sendMessage() {
            let input = document.getElementById("input").value;
            if (input.trim() === "") return;
            let chatbox = document.getElementById("chatbox");
            chatbox.innerHTML += '<div class="message user">' + input + '</div>';
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input })
            })
            .then(response => response.json())
            .then(data => {
                chatbox.innerHTML += '<div class="message bot">' + data.reply + '</div>';
                chatbox.scrollTop = chatbox.scrollHeight;
            });
            document.getElementById("input").value = "";
        }
    </script>
</body>
</html>
"""

# Route to serve the chatbot webpage
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Route to handle chatbot messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message').lower()
    if 'hours' in user_message or 'order time' in user_message or 'when can i order' in user_message or 'how far in advance' in user_message or 'days' in user_message or 'order' in user_message:
        reply = responses['hours']
    elif 'contact' in user_message or 'reach you' in user_message or 'phone number' in user_message or 'how to pay' in user_message or 'payment methods' in user_message:
        reply = responses['contact']
    elif 'location' in user_message or 'where are you' in user_message or 'pickup location' in user_message or 'delivery area' in user_message or 'where can i get my order' in user_message:
        reply = responses['location']
    elif 'price' in user_message or 'prices' in user_message or 'cost' in user_message or 'costs' in user_message or 'money' in user_message:
        reply = responses['prices']
    else:
        reply = responses['menu']  # Redirect most questions to the menu page
    return jsonify({'reply': reply + "Is that all, or do you have more questions?"})

if __name__ == '__main__':
    # Get the port from the environment variable, default to 5000 for local testing
    port = int(os.getenv('PORT', 5000))
    # Ensure the app binds to 0.0.0.0 for external access
    app.run(host='0.0.0.0', port=port, debug=False)