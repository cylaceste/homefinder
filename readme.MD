![logo](https://github.com/cylaceste/homefinder/blob/main/homefinder/frontend/src/images/logo.png)

# Homefinder: Your Digital Real Estate Navigator
Homefinder is an application that bridges the gap between OpenAI's powerful language model, your database, and users that don’t want to fiddle with filters and dropdown menus, creating an interface where AI can interact with your database and users. Basically, it makes OpenAI into a real estate agent that is familiar with your database and can use the database to provide information to users and suggest homes. We’ve also created a front-end for the user to interact with OpenAI. 

## Key Features:
-Dynamic Interaction with Database: Homefinder enables OpenAI's GPT-4 to access and interact with your database, any database, as if it was its own internal memory by providing the database schema. This seamless integration allows the AI to construct intricate queries runnable on your database, deep-dive into your data, and provide accurate, context-specific responses based on user messages.

-Intelligent Augmentation: Homefinder takes user messages, enriches them with instructions compatible with GPT-4's operation, and helps the AI design precise database queries. The database queries are quite inventive, for example using just latitude and longitude, queries are constructed that can filter neighbourhoods in the absence of neighbourhood information in the database!

-Database Schema Integration: Homefinder is built with a flexible architecture that allows it to incorporate your database schema, facilitating the AI's understanding of your data structure and thus ensuring high precision in data handling and query design.

-User-friendly Interface: To give you a hands-on feel of our product, Homefinder is equipped with an intuitive user interface that you can utilize to test the performance and responsiveness of our product, in real time. This includes a chatbox between the user and OpenAI (while hiding the interactions between OpenAI and your database) and a map feature that pins home locations and provides pictures and information about the homes. 

Homefinder is more than just an app; it's your virtual real estate agent that harnesses the power of OpenAI and your database to provide you with an unmatched property-finding experience.

Diagram:

Installation instructions:
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



Contributor Expectations:
We believe in the power of collaboration, and we welcome contributions from developers, designers, and data experts. If you're passionate about making housing search more accessible and efficient, we invite you to be a part of our community-driven development. Please follow the guidelines provided in our GitHub repository [Link to Contribution Guidelines] to contribute effectively.

Known issues:
1. Large prompts may result in incomplete responses from ChatGPT. We are actively working on improving prompt engineering to handle specific needs better.
2. Some complex database structures may require fine-tuning for seamless integration. If you encounter any issues, please report them, and we'll strive to enhance compatibility.
3. Errors can occur if the query from OpenAI is invalid. The solution is to re-run the command or pass the error along to OpenAI so it can amend the query. For performance, we propose using concurrency control; multithreaded calls to openAI and running the query returned, using the first response returned and passing it back to the user.


