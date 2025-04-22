# Personal Research Assistant

Welcome to the **Personal Research Assistant**, a web-based application designed to assist users in conducting research by leveraging AI-powered responses and storing conversation history. This project features a frontend built with HTML, CSS, and JavaScript, and a backend powered by FastAPI with MongoDB for data persistence.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [Contact](#contact)

## Features
- **AI-Powered Research**: Get detailed responses to research queries using the `/research` endpoint.
- **Conversation Storage**: Save and manage chat sessions via the `/store_conversations` endpoint.
- **User Authentication**: Secure access with JWT-based authentication.
- **Responsive Design**: Beautiful and user-friendly interface optimized for desktop and mobile.
- **Clickable Citations**: Research responses include linked sources for further reading.

## Prerequisites
- **Python 3.11+**: For the backend.
- **Node.js**: For running the frontend locally (optional, via `live-server`).
- **MongoDB**: A MongoDB instance (e.g., MongoDB Atlas) for data storage.
- **Git**: For version control and deployment.
- **npm**: For managing frontend dependencies (optional).

## Installation

### Clone the Repository
- git clone https://github.com/VasuGadde0203/Personal-Research-Assistant.git
- cd Personal-Research-Assistant

## Backend Setup
- Navigate to the backend directory:
  - cd backend
- Create a virtual environment and activate it:
  - python -m venv venv
  - source venv/bin/activate  # On Windows: venv\Scripts\activate
- Install dependencies:
  - pip install -r requirements.txt
- Create a .env file with the following variables:
  - MONGO_URI=YOUR_MONGO_URI
  - SERPAPI_API_KEY=YOUR_SERPAPI_KEY 
  - JWT_SECRET_KEY=YOUR_JWT_SECRET_KEY
  - AZURE_OPENAI_API_KEY = AZURE_OPENAI_KEY
  - AZURE_OPENAI_ENDPOINT = YOUR_AZURE_OPENAI_ENDPOINT
  - AZURE_OPENAI_API_VERSION= YOUR_AZURE_OPENAI_API_VERSION
  - AZURE_OPENAI_DEPLOYMENT_NAME = AZURE_OPENAI_DEPLOYMENT_NAME

- Run the FastAPI server:
  - uvicorn main:app --reload
  - Access at http://localhost:8000

## Frontend Setup
- Navigate to the frontend directory:
  - cd ../chatbot-frontend
- Install live-server globally (optional, for local testing):
  - npm install -g live-server
- Start the frontend:
  - live-server
- Access at http://localhost:8080.

## Usage
- Open the app in your browser (e.g., http://localhost:8080 or deployed URL).
- Sign in with your credentials (configured via the /auth/login endpoint).
- Type a research query (e.g., "Impact of remote work") and press "Send".
- View the AI-generated response with clickable citations.
- The conversation is automatically saved to the backend.

## Deployment
- This app is designed to be deployed using Render (for the backend) and Netlify (for the frontend). Below are the steps for future deployment:

### Backend Deployment on Render
- Sign up at render.com.
- Connect your GitHub repository and select the backend folder.
- Set environment variables (MONGO_URI, SECRET_KEY, PORT=10000) in Render.
- Deploy with the build command pip install -r requirements.txt and start command web: uvicorn main:app --host 0.0.0.0 --port $PORT.
  
### Frontend Deployment on Netlify
- Sign up at netlify.com.
- Connect your GitHub repository and set the publish directory to chatbot-frontend.
- Deploy the site.
- Update scripts.js with the Render backend URL (e.g., const API_BASE_URL = 'https://your-app.onrender.com';) after backend deployment.

### Deployed URLs
- (Will be updated with actual URLs once deployed.)

## API Endpoints
- /research/ (POST): Get AI research responses.
  - Body: { "topic": "string", "max_results": int }
  - Headers: Authorization: Bearer <token>
- /chats/store_conversations (POST): Save a conversation.
  - Body: { "title": "string", "messages": [{ "role": "string", "content": "string|dict" }] }
  - Headers: Authorization: Bearer <token>
- /auth/login (POST): Authenticate and get a JWT token.
  - Body: { "email": "string", "password": "string" }
    
## Contributing
- Fork the repository.
- Create a feature branch (git checkout -b feature-name).
- Commit your changes (git commit -m "Add feature").
- Push to the branch (git push origin feature-name).
- Open a pull request.

## Contact
- Author: Vasu Gadde
- GitHub: VasuGadde0203
- Email: vasugadde0203@gmail.com
