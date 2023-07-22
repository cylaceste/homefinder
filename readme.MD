# homefinder
TODO Describe the app


## Frontend
1. Install nodejs from https://nodejs.org/en

2. From the root directory run the following to cd into the frontend application and start it. Be patient!
```
cd homefinder/frontend
npm start
```

## Backend

1. Set your openai key:
```
export OPENAI_KEY=<your_openai_key>
```
or if you're on Windows use:
```
set OPENAI_KEY=<your_openai_key>
```

2. Install requirements. From root directory, use your terminal to run:
```
pip install -r homefinder/requirements.txt
```

3. Start the server
```
python homefinder/backend/server.py
```