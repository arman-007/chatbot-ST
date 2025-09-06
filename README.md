# Backend AI Chatbot with RAG Pipeline

## Project Overview
This is a backend service for an AI chatbot that uses a **Retrieval-Augmented Generation (RAG)** pipeline to provide context-aware responses.  
It features user authentication, stores chat history, and handles background tasks for maintenance.  
The service is built with the **Django Rest Framework** and leverages a local **Ollama** model for generative AI capabilities.

---

## Technologies Used
- **Backend Framework:** Django Rest Framework  
- **Database:** SQLite  
- **Authentication:** JSON Web Tokens (JWT)  
- **RAG Pipeline:** FAISS (for vector search) and sentence-transformers (for embeddings)  
- **AI Model:** Ollama with the **phi3:mini** model  
- **Background Tasks:** APScheduler (for task scheduling)  

---

## Project Setup

### Prerequisites
- Python 3.8+  
- pip package manager

### Ollama Setup
1. Download and install Ollama from [ollama.ai](https://ollama.ai).  
2. Ensure the Ollama service is running on your local machine.  
3. Pull the **phi3:mini** model by running:  
   ```bash
   ollama pull phi3:mini
   ```

### Clone the Repository
```bash
git clone https://github.com/arman-007/chatbot-ST
cd chatbot-ST
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Run the Server
```bash
python manage.py runserver
```

---

## API Endpoints

### **POST /signup**
Registers a new user.  
**Request Body:**  
```json
{
  "username": "user",
  "email": "user@example.com",
  "password": "password123"
}
```

---

### **POST /login**
Authenticates a user and returns a JWT token.  
**Request Body:**  
```json
{
  "username": "user",
  "password": "password123"
}
```  
**Response:**  
```json
{
  "token": "your_jwt_token"
}
```

---

### **GET /chat-history**
Retrieves the chat history for the logged-in user.  
**Authentication:** Requires a valid JWT token in the Authorization header:  
```
Bearer <token>
```

---

### **POST /chat**
Sends a message to the chatbot and receives a response. The message and response are saved to chat history.  
**Request Body:**  
```json
{
  "message": "Hello, what is RAG?"
}
```  
**Authentication:** Requires a valid JWT token.

---

## Answers to README Questions

### How did you integrate the RAG pipeline?
The RAG pipeline is integrated using **sentence-transformers** for creating vector embeddings of the knowledge base documents. These embeddings are stored in a **FAISS index**, which is used to perform a vector-based similarity search. Retrieved documents are included as context in the prompt sent to the local Ollama model to generate a context-aware response.

### What database and model structure did you use?
The project uses Django's ORM, with PostgreSQL or SQLite. Chat history is stored in a `ChatHistory` model linked to users. Fields include:
- user (ForeignKey to Django's User model)
- user_message
- chatbot_response
- timestamp

### How did you implement user authentication using JWT?
JWT tokens are issued on successful login. Clients send this token in the Authorization header for protected endpoints. The backend validates tokens without storing session state.

### How does the chatbot generate responses?
1. Retrieve relevant documents with the RAG pipeline.  
2. Construct a prompt including the user's query and retrieved context.  
3. Send the augmented prompt to the **phi3:mini** model via Ollama.  
If no relevant documents are found, a general answer is provided.

### How did you schedule and implement background tasks?
Background tasks are managed using **APScheduler**. A daily job `delete_old_chat_history` deletes records older than 30 days to prevent excessive database growth.

### What testing strategies did you use?
- Functional tests: Verified RAG retrieval and response generation.  
- Integration tests: Verified API endpoints (signup, login, chat, chat-history) using tools like Postman.  

### What external services did you integrate?
- **Ollama**: Local LLM server for responses.  
- **FAISS**: For similarity search in vector DB.  
- **sentence-transformers**: For dense embeddings.  

### How would you expand this chatbot?
- Real-time knowledge base updates with auto re-indexing.  
- Multi-user chat sessions (chat rooms/groups).  
- WebSockets for real-time chat functionality.  

---

## Run Ollama and Model Setup Recap
Make sure Ollama is running before using the chatbot:  
```bash
ollama run phi3:mini
```