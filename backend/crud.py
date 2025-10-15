from sqlalchemy.orm import Session
import models, schemas, auth
from uuid import uuid4
from datetime import datetime

# -------------------- USER --------------------

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = auth.hash_password(user.password)
    db_user = models.User(
        user_name=user.user_name,
        user_email=user.user_email,
        password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.user_email == email).first()
    if user and auth.verify_password(password, user.password):
        return user
    return None

# -------------------- NOTES --------------------

# Create new note
def create_note(db: Session, user_id: str, note: schemas.NoteBase):
    db_note = models.Note(
        note_id=str(uuid4()),   # unique ID for note
        user_id=user_id,
        note_title=note.note_title,
        note_content=note.note_content,
        created_on=datetime.utcnow()
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# Get all notes for a user
def get_notes(db: Session, user_id: str):
    return db.query(models.Note).filter(models.Note.user_id == user_id).all()


# Get a single note by ID
def get_note_by_id(db: Session, note_id: str):
    return db.query(models.Note).filter(models.Note.note_id == note_id).first()


# Update a note
def update_note(db: Session, note_id: str, note_update: schemas.NoteBase):
    note = db.query(models.Note).filter(models.Note.note_id == note_id).first()
    if not note:
        return None
    note.note_title = note_update.note_title
    note.note_content = note_update.note_content
    note.updated_on = datetime.utcnow()
    db.commit()
    db.refresh(note)
    return note


# Delete a note
def delete_note(db: Session, note_id: str):
    note = db.query(models.Note).filter(models.Note.note_id == note_id).first()
    if not note:
        return False
    db.delete(note)
    db.commit()
    return True
