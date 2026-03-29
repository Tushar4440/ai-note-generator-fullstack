# AI Note Generator Fullstack

## Overview
This project is a fullstack AI Note Generator app with a Python FastAPI backend and a React/Vite frontend.

- Backend: `backend/`
  - `main.py` (FastAPI app entry)
  - `auth.py` (authentication logic)
  - `database.py` (DB setup)
  - `models.py` (Pydantic/ORM models)
  - `gemini.py` (AI generation integration)

- Frontend: `frontend/`
  - React app built with Vite
  - `src/App.jsx`, `src/main.jsx`, `src/index.css`

## Requirements
- Python 3.10+
- Node.js 16+

## Setup
### Backend
1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. `uvicorn main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Usage
- Backend: `http://localhost:8000`
- Frontend: typically `http://localhost:5173`

## Notes
- If using an AI API key (Gemini or similar), add it to environment variables in the backend.
- Make sure the backend endpoint URL is configured in the frontend if they run on different hosts.
