![logo](https://github.com/cylaceste/homefinder/blob/main/homefinder/frontend/src/images/logo.png)

# homefinder
homefinder bridges the gap between users and the database in a modern way, without clunky filters but with natural language. homefinder is an application that is built on React as a front end and Flask as a backend. It works by messaging OpenAI'

## Frontend
1. Install nodejs from https://nodejs.org/en

2. From the root directory run the following to cd into the frontend application, install packages and start the app. Be patient!
```
cd homefinder/frontend
npm install
npm start
```

## Backend

1. Set your openai key:
```
export OPENAI_API_KEY=<your_openai_key>
```
or if you're on Windows use:
```
set OPENAI_API_KEY=<your_openai_key>
```

2. Install requirements. From root directory, use your terminal to run:
```
pip install -r homefinder/backend/requirements.txt
```

3. Start the server
```
python homefinder/backend/server.py
```
