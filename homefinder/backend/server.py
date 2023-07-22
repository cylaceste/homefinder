from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from your React app

@app.route('/send_message', methods=['POST'])
def send_message():
    message_history = request.get_json()  # Get the message history from the request

    # Logic for getting agent's response
    agent_response = get_agent_response(message_history)

    return jsonify({"agent": agent_response})

def get_agent_response(message_history):
    # Implement your logic for generating the agent's response here
    # For simplicity, let's just echo back the last user's message
    last_user_message = [message["user"] for message in message_history if "user" in message][-1]
    return f"ECHO: {last_user_message}"

@app.route('/get_locations', methods=['GET'])
def get_locations():
    # This is where you'd typically fetch these locations from your database
    # For this example, I'm returning a static list of locations
    locations = [
        {
            "latitude": 52.505,
            "longitude": -0.09,
            "info": "Location 1"
        },
        {
            "latitude": 51.51,
            "longitude": -0.1,
            "info": "Location 2"
        }
    ]
    
    return jsonify(locations)

if __name__ == '__main__':
    app.run(debug=True)
