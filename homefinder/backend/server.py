from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from typing import Dict, List, Any
import openai
import ast
from dataclasses import dataclass
import json


current_file_directory = os.path.dirname(os.path.realpath(__file__))
database_dir = os.path.join(current_file_directory,'..','database')
sys.path.insert(0, database_dir)
from database import Database

DATABASE_TYPE = "SQLite"

def sterilize_string(string: str) -> str:
    return string.replace('\n', ' ').replace('  ', ' ')


openai.api_key = "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" # os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
CORS(app)  # Allow requests from your React app
property_database = Database()
"Store prompt components to keep things DRY"
pc = {"preamble": """You are a real estate assistant helping guide a user buy or rent a home in Calgary or Edmonton. 
Your task is to return a JSON formatted string without any additional text.
Do not include any introductory or concluding text. Your response should be strictly 
the JSON formatted string.""",
    "schema": f"""The schema for the database is {property_database.get_database_definition()}.""",
    "query_for_info": f"""You can, optionally, query the {DATABASE_TYPE} database by returning a
response that looks like json formatted string 
like {{"query_for_info": your_db_query_here}} and with no other keys or text, then system
will run this query on the database and return the information to you. 
your_db_query_here must be a {DATABASE_TYPE} query that uses things that would exist
based on the provided schema. Remember to limit your query with a LIMIT 10 or something similar
or it will be too much info to pass back. Only do this if you need information, for example, 
an agents phone number or to retrieve information to answer a query from the user or 
a hunch you might have.""",
    "query_response": f"""You can respond back to the user by providing a json formatted string
that has the form {{"sql_query": sql_query, "assistant_response": assistant_response}} with
no other keys or text other than what's in the json.
For sql_query, given the database schema and the conversation with the user, and any
information you received from system, write a sql_query to fetch 10 properties 
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
prompt the user for more information."""}

@app.route('/send_message', methods=['POST'])
def send_message():
    message_history = request.get_json()  # Get the message history from the request

    # Logic for getting agent's response
    return get_agent_response(message_history)

def get_agent_response(message_history: List[Dict[str, str]]):
    '''
    message_history should look like List[{"role": user, "content": message}]
    '''
    sql_table_query = ''

    prompt_messages = [{
        "role": "system",
        "content": "\n".join([sterilize_string(string) for string in [pc["preamble"], pc["schema"], pc["query_for_info"], pc["query_response"]]])

    }]
    
    prompt_messages += message_history

    for _ in range(2):
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=prompt_messages,
        #     temperature=0,
        #     max_tokens=4096
        # )
        # print('here2')
        # response_content = response['choices'][0]['message']['content']
        response_content = """{"sql_query": "SELECT property_table.property_name, property_table.description, property_table.num_bedroom, property_table.num_bathroom, property_table.area_size, property_table.price, property_table.transaction_type, property_table.property_type, property_table.parking, property_table.laundry, property_table.furnished, property_table.pet_friendly, property_table.latitude, property_table.longitude, property_table.build_year, property_table.smoking_allowed, property_table.air_conditioning, property_table.hardwood_floors, property_table.balcony, GROUP_CONCAT(image_table.image_url) as image_urls FROM property_table LEFT JOIN image_table ON property_table.property_id = image_table.property_id WHERE property_table.num_bedroom >= 5 AND property_table.property_type = 'House' GROUP BY property_table.property_id LIMIT 10", "assistant_response": "I'm showing you houses with at least 5 bedrooms to accommodate you and your 4 kids. Do you have a preference for the location, budget, or any specific amenities (like a garage, air conditioning, etc.)?"}"""
        response_dict: Dict[str, str] = ast.literal_eval(response_content)
        query_for_info = response_dict.get('query_for_info', '')
        if query_for_info:
            sql_query_result = json.dumps(property_database.fetch_query(query_for_info))
            # Remove the query_for_info prompt component
            # Presumably we don't want to query the database multiple times
            # As that would take too long
            prompt_messages[0]['content'] = "\n".join([sterilize_string(string) for string in [pc["preamble"], pc["schema"], pc["query_response"]]])
            prompt_messages.append({
                "role": "system",
                "content": sql_query_result
                })
        else:
            query_from_gpt = response_dict['sql_query']
            response_payload = {"properties": get_locations(query_from_gpt),
            "message_history": message_history + [response_dict['assistant_response']]
            }
            print('payload')
            print(response_payload)
            return response_payload
    return 500

def get_locations(query: str) -> List[Dict[str, Any]]:
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
    return locations


if __name__ == '__main__':
    app.run(debug=True)
