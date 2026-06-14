from models import Email
from sqlalchemy.orm import Session
from schemas import Email_Create


def send_email(db: Session, data: Email_Create):
    email_send = Email(**data.model_dump())
    db.add(email_send)
    db.commit()
    db.refresh(email_send)

    return email_send


def receive_email(db: Session):
    return db.query(Email).all()


def delete_email(db: Session, id: int):
    email_by_id = db.query(Email).filter(Email.email_id == id).first()

    if email_by_id:
        db.delete(email_by_id)

    db.commit()
    return email_by_id
