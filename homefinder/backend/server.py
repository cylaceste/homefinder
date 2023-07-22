from flask import Flask, render_template, jsonify, request
import openai
import json
import concurrent.futures
import os

TEMPLATE_DIR: str = os.path.join(os.path.dirname(__file__), 'templates')
app: Flask = Flask(__name__, template_folder=TEMPLATE_DIR)

openai.api_key = os.getenv("OPENAI_KEY")

@app.route('/', methods=['GET'])
def index() -> str:
    return 200, 'Found route!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
