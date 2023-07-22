from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
current_file_directory = os.path.dirname(os.path.realpath(__file__))
database_dir = os.path.join(current_file_directory,'..','database')
sys.path.insert(0, database_dir)
from database import PropertyDatabase

app = Flask(__name__)
CORS(app)  # Allow requests from your React app
property_database = PropertyDatabase()
row = [1, 'Property name', 'Description', 2, 1, 100, 50000.00, 'Buy', 'Condo', 'garage', 'in_suite', True, False, 0.0000000, 0.0000000, 2000, False, True, True, False]
property_database.insert_row('property_table', row)

# Insert multiple rows
rows = [
    [2, 'Property name 2', 'Description 2', 3, 2, 150, 60000.00, 'Rent', 'Apartment', 'underground', 'shared', False, True, 1.0000000, 1.0000000, 2001, True, False, False, True],
    [3, 'Property name 3', 'Description 3', 4, 3, 200, 70000.00, 'Buy', 'House', 'covered', 'in_suite', True, False, 2.0000000, 2.0000000, 2002, False, True, True, False]
]
property_database.insert_row('property_table', rows)
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
    properties = property_database.fetch_query(query)
    locations = [
        {
            "latitude": property[14],
            "longitude": property[15],
            "info": f"Property Name: {property[1]} \n Description: {property[2]}"
        } for property in properties
    ]
    return jsonify(locations)


if __name__ == '__main__':
    app.run(debug=True)
