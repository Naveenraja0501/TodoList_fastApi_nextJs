# TO do List App

A **To-Do List application** built with **Next.js** for the frontend and **FastAPI** for the backend.  
Users can register/login, add, update, and delete their tasks. Authentication is handled using **JWT**, and **MySQL** is used as the database.

---

## Project Overview

- **Frontend:** Next.js + HTML + CSS + JavaScript  
- **Backend:** FastAPI + JWT for authentication  
- **Database:** MySQL  
- **Features:**
  - User registration and login
  - JWT-based authentication
  - Add, edit, and delete tasks
  - Responsive UI
  - Notifications for actions (success/error)

---

## Getting Started

### Frontend

1. Navigate to the frontend folder:

```bash
cd frontend

npm install

npm run dev

### Backend

Navigate to the backend folder:

cd backend

pip install -r requirements.txt

uvicorn main:app --reload