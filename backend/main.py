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

# ------------------ AUTH ------------------
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

# ------------------ NOTES CRUD ------------------

# Get all notes for a user
@app.get("/notes")
def get_notes(user_id: str, db: Session = Depends(get_db)):
    return crud.get_notes(db, user_id)

# Create a new note
@app.post("/notes")
def create_note(user_id: str, note: schemas.NoteBase, db: Session = Depends(get_db)):
    return crud.create_note(db, user_id, note)

# Get single note by ID
@app.get("/notes/{note_id}")
def get_note(note_id: str, db: Session = Depends(get_db)):
    note = crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# Update note
@app.put("/notes/{note_id}")
def update_note(note_id: str, note_update: schemas.NoteBase, db: Session = Depends(get_db)):
    updated_note = crud.update_note(db, note_id, note_update)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note

# Delete note
@app.delete("/notes/{note_id}")
def delete_note(note_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_note(db, note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}
