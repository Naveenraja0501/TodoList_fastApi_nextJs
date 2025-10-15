from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import database
import models
import schemas
import crud
import auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.user_email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_access_token({"sub": db_user.user_id})
    return {"access_token": token, "user_id": db_user.user_id}

@app.get("/notes")
def get_notes(user_id: str, db: Session = Depends(get_db)):
    return crud.get_notes(db, user_id)

@app.post("/notes")
def create_note(user_id: str, note: schemas.NoteBase, db: Session = Depends(get_db)):
    return crud.create_note(db, user_id, note)

