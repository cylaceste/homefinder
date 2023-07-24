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


openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
CORS(app)  # Allow requests from your React app
property_database = Database()
"Store prompt components to keep things DRY"
pc = {"preamble": """You are a real estate assistant helping guide a user buy or rent a home in     Edmonton. 
Your task is to return a JSON formatted string without any additional text.
Do not include any introductory or concluding text. Your response should be strictly 
the JSON formatted string.""",
    "schema": f"""The schema for the database is {property_database.get_database_definition()}.""",
    "query_for_info": f"""
Optionally, you can query the {DATABASE_TYPE} database. To do this, provide a JSON string in the format {{"query_for_info": your_db_query_here}}. The system will execute the query and return the results. 

Ensure that 'your_db_query_here' is a valid {DATABASE_TYPE} query, based on the provided schema. To manage the data volume, limit your query with a 'LIMIT 10' or similar clause. 

Use this feature if you need specific details, such as an agent's phone number, or to respond to user queries based on a particular hunch.
""",
    "query_response": f"""
To respond, provide a JSON string with the format {{"sql_query": sql_query, "assistant_response": assistant_response}}. 'sql_query' should be a query that fetches 10 properties with the columns: latitude, longitude, and property_description. Ensure to include these regardless of the query. Based on the database schema, rename these columns if needed. Also include an 'image_urls' column with a comma-separated list of images for each property. 

Include additional columns if relevant to the user but avoid unnecessary ones like table keys. Make sure to filter the data based on user conversation using a WHERE clause. Specify the table source when joining statements, and remember to use only columns from the schema. Creativity is key; for instance, if a user wants properties in Edmonton or Calgary, use the latitude and longitude to define these areas in your WHERE clause.

'assistant_response' should describe the properties shown and why they were chosen based on the filters used. Don't mention how many homes you are showing. It should also pose a question to the user that will help refine your query, explaining why the question is necessary. Prioritize questions that a real estate agent would ask, like intent to buy or rent and budget. 

If you lack sufficient data, generate a generic query and ask the user for more details.
"""
}

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
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=prompt_messages,
            temperature=0,
            max_tokens=4096
        )
        response_content = response['choices'][0]['message']['content']
        # response_content = """{"sql_query": "SELECT property_table.property_name, property_table.description, property_table.num_bedroom, property_table.num_bathroom, property_table.area_size, property_table.price, property_table.transaction_type, property_table.property_type, property_table.parking, property_table.laundry, property_table.furnished, property_table.pet_friendly, property_table.latitude, property_table.longitude, property_table.build_year, property_table.smoking_allowed, property_table.air_conditioning, property_table.hardwood_floors, property_table.balcony, GROUP_CONCAT(image_table.image_url) as image_urls FROM property_table LEFT JOIN image_table ON property_table.property_id = image_table.property_id WHERE property_table.num_bedroom >= 5 AND property_table.property_type = 'House' GROUP BY property_table.property_id LIMIT 10", "assistant_response": "I'm showing you houses with at least 5 bedrooms to accommodate you and your 4 kids. Do you have a preference for the location, budget, or any specific amenities (like a garage, air conditioning, etc.)?"}"""
        response_dict: Dict[str, str] = ast.literal_eval(response_content)
        query_for_info = response_dict.get('query_for_info', '')
        if query_for_info:
            print('query for info:', query_for_info)
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
            query_from_gpt = response_dict.get('sql_query', '')
            print('query_from_gpt:', query_from_gpt)
            response_payload = {"properties": get_locations(query_from_gpt) if query_from_gpt else [],
            "message_history": message_history + [{"role": "assistant", "content": response_dict['assistant_response']}]
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
            "image_urls": property.get('image_urls', ''),
        } for property in properties
    ]
    return locations


if __name__ == '__main__':
    app.run(debug=True)
