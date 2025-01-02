# Running Frontend and Backend Projects Simultaneously

To run both the frontend and backend projects at the same time, follow these steps:


### Step 1: Start the FastAPI Backend Server

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Start the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   This starts the server on http://localhost:8000.

### Step 2: Start the React Frontend Server

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Start the frontend server:
   ```bash
   npm start
   ```
   This starts React on http://localhost:3000

### Step 3: Open Your Browser
Navigate to http://localhost:3000. You should see the chat interface. Ask a question, and the system will perform retrieval + generation using your PDF or text documents as context.
