from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import SessionLocal, engine, Base
from models import User, UserInput, Note
from auth import hash_password, verify_password, create_token, decode_token
from gemini import generate_notes
from fastapi.middleware.cors import CORSMiddleware

# Creating fastapi app
app = FastAPI()  

# add cors middle ware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Defines how tokens are retrived 
security = HTTPBearer()

# Creates a new databse session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Register
@app.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(400, "User already exists")

    new_user = User(email=email, password=hash_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "Registered Successfully"}


# login
@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(401, "Invalid Credentials")

    token = create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


# get current user
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials.replace("Bearer ", "")
        # print("token recieved",token)

        payload = decode_token(token)
        # print("Decode Payload", payload)

        user_id = payload.get("sub")
        print("User id ", user_id)

        if user_id is None:
            raise HTTPException(401, "Invalid Token")
        return int(user_id)
    except Exception as e:
        print("TOKEN ERROR :", e)
        raise HTTPException(status_code=401, detail="Invalid Token")


# submit input
@app.post("/generate-notes")
def generate(
    content: str,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Save input
    new_input = UserInput(user_id=user_id, content=content)
    db.add(new_input)
    db.commit()

    # Get last 5 inputs (context memory)
    past = (
        db.query(UserInput)
        .filter(UserInput.user_id == user_id)
        .order_by(UserInput.id.desc())
        .limit(5)
        .all()
    )

    # Build context safelly
    context = "\n".join([str(p.content) for p in past][::-1])

    # Generate notes with gemini
    try:
        notes = generate_notes(context, content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")
    
    # Save generated notes
    new_note = Note(user_id=user_id, content=notes)
    db.add(new_note)
    db.commit()

    return {"notes": notes}


# Get notes
@app.get("/notes")
def get_notes(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    return notes


# Deleting note
@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int, 
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(Note.id == note_id,Note.user_id == user_id).first()
    if not note:
        raise HTTPException(404, "Note not found or not authorised")
    db.delete(note)
    db.commit()
    return {"msg": "Note deleted successfully"}

# Updating a note
@app.put("/note/{note_id}")
def update_note(
    note_id: int,
    new_content: str,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or not authorised")

    db.query(Note).filter(Note.id == note_id, Note.user_id== user_id).update({"content": new_content})
    db.commit()
    db.refresh(note)

    return {"msg": "Note updated successfully"}