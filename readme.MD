
# TODO 
Describe the app

Finish Front end and beautify

Add more info to database


# homefinder

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
