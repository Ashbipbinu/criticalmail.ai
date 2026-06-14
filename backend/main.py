import services
import schemas

from fastapi import FastAPI, Depends
from db import get_db
from sqlalchemy.orm import Session
from db import create_db

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()


@app.on_event("startup")
def startup():
    create_db()


@app.get("/")
def get_server_status():
    return "Server is active and ready to receive requests"


@app.get("/receive_emails", response_model=list[schemas.Email])
def get_emails(db: Session = Depends(get_db)):
    try:
        logging.info("Initialized getting emails")
        all_emails = services.receive_email(db)
        return all_emails

    except Exception as ex:
        logging.error("Failed to get email", exc_info=True)
        raise ex


@app.post("/send-email", response_model=schemas.Email)
def create_email(data: schemas.Email_Create, db: Session = Depends(get_db)):
    try:
        logging.info("Initialized sending mail")

        models_prediction = 0
        email_dict = data.model_dump()
        email_dict["model_prediction"] = models_prediction

        created_email = services.send_email(db, data)
        if created_email:
            logging.info("Email sent completed")
            return created_email

    except Exception as ex:
        logging.error("Failed to receive email", exc_info=True)
        raise ex


@app.delete("/delete-email/{id}", response_model=schemas.Email)
def delete_email(id: int, db: Session = Depends(get_db)):
    try:
        logging.info("Initilizing email deletion")
        deleted_email = services.delete_email(db, id)
        if deleted_email:
            logging.info("Deletion completed")
            return deleted_email

    except Exception as ex:
        logging.error("Failed to delete email", exc_info=True)
        raise ex
