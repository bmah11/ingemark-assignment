
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, security
from .database import SessionLocal, engine, Base
from typing import List
from uuid import UUID

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/messages/", response_model=schemas.Message, dependencies=[Depends(security.get_api_key)])
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_message = models.Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/messages/", response_model=List[schemas.Message], dependencies=[Depends(security.get_api_key)])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = db.query(models.Message).offset(skip).limit(limit).all()
    return messages

@app.put("/messages/{message_id}", response_model=schemas.Message, dependencies=[Depends(security.get_api_key)])
def update_message(message_id: UUID, message: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_message = db.query(models.Message).filter(models.Message.message_id == message_id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    for var, value in vars(message).items():
        setattr(db_message, var, value) if value is not None else None

    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
