from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

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
    # last_user_message = [message["user"] for message in message_history if "user" in message][-1]

    openai.api_key = os.getenv("OPENAI_API_KEY")
    sql_table_query =
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

    # return f"ECHO: {last_user_message}"
    return f"ECHO: {response_content}"

if __name__ == '__main__':
    app.run(debug=True)
