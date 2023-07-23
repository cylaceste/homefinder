from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from typing import Dict, List, Any
current_file_directory = os.path.dirname(os.path.realpath(__file__))
database_dir = os.path.join(current_file_directory,'..','database')
sys.path.insert(0, database_dir)
from database import Database
import openai

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
    openai.api_key = os.getenv("OPENAI_API_KEY")
    sql_table_query = \
"""
CREATE TABLE edmonton_rent_property_table (
    pk_column propertyId PRIMARY KEY,
    property_name VARCHAR(255),
    description VARCHAR,
    num_bedroom INT,
    num_bathroom INT,
    area_size INT,
    furnished BOOL,
    pet_friendly BOOL,
    thrumb_nail VARCHAR,
    Inside_figure VARCHAR,
    Outside_figure VARCHAR,
    Geolocation VARCHAR,
    property_types ENUM(Condo, Apartment, House),
    build_year YEAR,
);
"""

    prompt_messages = [{
        "role": "system",
        "content": "Given the following SQL tables, your job is to write "
        "queries given a user’s request. Return only the query, your "
        "response should start with INSERT INTO and your entire text "
        "response should be runnable.\n\n{sql_table_query}"
    }]
    for message in message_history:
        if 'user' in message:
            prompt_messages.append({
                'role': 'user',
                'content': message['user']
            })
        if 'assistant' in message:
            prompt_messages.append({
                'role': 'assistant',
                'content': message['assistant']
            })

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=prompt_messages,
        temperature=0,
        max_tokens=1024
    )
    response_content = response['choices'][0]['message']['content']
    message_history[-1]['assistant'] = response_content

    return f"ECHO: {response_content}"

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
