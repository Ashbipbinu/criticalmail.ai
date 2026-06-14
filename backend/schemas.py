from pydantic import BaseModel
from datetime import date


class Email_Create(BaseModel):
    name: str
    sender_email: str
    subject: str
    body: str


class Email(Email_Create):
    email_id: int
    date_sent: date
    model_prediction: int

    class config:
        from_attributes = True
