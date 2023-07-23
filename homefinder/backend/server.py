from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from typing import Dict, List, Any
import openai
import ast


current_file_directory = os.path.dirname(os.path.realpath(__file__))
database_dir = os.path.join(current_file_directory,'..','database')
sys.path.insert(0, database_dir)
from database import Database

openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
CORS(app)  # Allow requests from your React app
property_database = Database()
@app.route('/send_message', methods=['POST'])
def send_message():
    message_history = request.get_json()  # Get the message history from the request

    # Logic for getting agent's response
    agent_response = get_agent_response(message_history)

    return jsonify({"agent": agent_response})

def get_agent_response(message_history: List[Dict[str, str]]):
    print(type(message_history))
    sql_table_query = ''

    prompt_messages = [{
        "role": "system",
        "content": 
        f"""You are a real estate assistant helping guide a user buy or rent a home. 
Your task is to return a JSON formatted string without any additional text, 
following this format: 
{{"sql_query": sql_query, "assistant_response": assistant_response}}
Do not include any introductory or concluding text. Your response should be strictly 
the JSON formatted string.
For context here is the SQLite database schema: \n {property_database.get_database_definition()}
For the sql_query, given the database schema and the conversation with the user, write a sql_query to fetch 10 properties 
and the following columns: latitude, longitude, property_description. Each database will be different 
and these columns may appear under different names, so be sure to rename the columns in the schema 
to these names. Also, return an image_urls column which contains a comma-separated list of all image urls 
which belong to each property. Return any additional columns the user might be interested in. 
Avoid columns that are not needed, probably the table keys, etc.
Be sure to add a where clause which filters based on information from the conversation with the user.
When writing join statements, be sure to include which table each column is coming from.
Remember that the only columns you can use are from the schema, so be creative. For example,
if the user asks for homes in Edmonton or Calgary, use the latitude and longitude in a where
clause to box these cities in.
For the assistant_response, explain that you're showing them properties you think they might 
be interested in, along with an explanation of what kind of homes you're showing based on the filter 
in the WHERE clause and why you picked each filter. Then, prompt the user with a question based on the database schema 
which will help you refine your query further and explain why you're asking that question. 
Prioritize questions that a real estate agent might ask, such as whether they plan to buy or rent,
or their budget
If you don't have enough information to do this, create a generic sql_query of homes and 
prompt the user for more information."""

    }]
    print(prompt_messages)
    prompt_messages += [{'role': key, 'content': message[key]} for message in message_history for key in message.keys()]
    return f"ECHO: {'hello!'}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=prompt_messages,
        temperature=0,
        max_tokens=1024
    )
    '''
    Sample response
    {
    "sql_query": "SELECT property_id, description AS property_description, latitude, longitude, GROUP_CONCAT(image_url) AS image_urls FROM property_table LEFT JOIN image_table ON property_table.property_id = image_table.property_id WHERE num_bedroom >= 8 AND pet_friendly = 1 AND latitude BETWEEN 49.61000 AND 49.75000 AND longitude BETWEEN -112.90000 AND -112.70000 GROUP BY property_table.property_id LIMIT 10;", 
    "assistant_response": "Based on your needs, I'm showing you properties that have at least 8 bedrooms and are pet-friendly, in the area approximate to Lethbridge, Alberta. I've used these filters because you mentioned having a large family and two dogs. To help me narrow down the options further, could you please let me know your budget range, and whether you are looking to rent or buy?"
    }

    '''
    response_content = response['choices'][0]['message']['content']
    response_dict = ast.literal_eval(response_content)
    response_dict.update({"properties": get_locations(response_dict['sql_query'])})
    return response_dict

@app.route('/get_locations', methods=['GET'])
def get_locations(query: str):
    properties, fields = property_database.fetch_query(query)
    properties: List[Dict[str, Any]] = [{fields[i]: property[i] for i in range(len(property))} for property in properties]

    non_info_columns = {'latitude', 'longitude', 'property_id', "image_url"}
    locations = [
        {
            "latitude": property['latitude'],
            "longitude": property['longitude'],
            "info": '\n'.join([f"{field_name}: {field_value}" for field_name, field_value in property.items() if field_name not in non_info_columns]),
            "image_urls": property['image_urls'],
        } for property in properties
    ]
    return jsonify(locations)


if __name__ == '__main__':
    app.run(debug=True)
