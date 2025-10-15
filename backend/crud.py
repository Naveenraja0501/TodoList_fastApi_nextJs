from sqlalchemy.orm import Session
import models, schemas, auth

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = auth.hash_password(user.password)
    db_user = models.User(user_name=user.user_name, user_email=user.user_email, password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.user_email == email).first()
    if user and auth.verify_password(password, user.password):
        return user
    return None

def create_note(db: Session, user_id: str, note: schemas.NoteBase):
    db_note = models.Note(user_id=user_id, **note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes(db: Session, user_id: str):
    return db.query(models.Note).filter(models.Note.user_id == user_id).all()
