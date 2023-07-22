from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from typing import Dict, List, Any
current_file_directory = os.path.dirname(os.path.realpath(__file__))
database_dir = os.path.join(current_file_directory,'..','database')
sys.path.insert(0, database_dir)
from database import Database

app = Flask(__name__)
CORS(app)  # Allow requests from your React app
property_database = Database()
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
    query = 'SELECT * FROM property_table;'
    properties, fields = property_database.fetch_query(query)
    properties: List[Dict[str, Any]] = [{fields[i]: property[i] for i in range(len(property))} for property in properties]
    locations = [
        {
            "latitude": property['latitude'],
            "longitude": property['longitude'],
            "info": '\n'.join([f"{field_name}: {field_value}" for field_name, field_value in property.items() if field_name not in {'latitude', 'longitude', 'property_id'}]),
            "images": [image_url for image_url in property_database.get_images_for_property_id(property['property_id'])],
            # "info": f"Property Name: {property[1]} \n Description: {property[2]}"
        } for property in properties
    ]
    return jsonify(locations)


if __name__ == '__main__':
    app.run(debug=True)
