from datetime import date
from sqlalchemy import Column, Integer, String, Date

from db import Base


class Email(Base):
    __tablename__ = "email"
    email_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, primary_key=False, index=True)
    sender_email = Column(String, primary_key=False, index=True)
    subject = Column(String, primary_key=False, index=False)
    body = Column(String, primary_key=False, index=False)
    date_sent = Column(Date, primary_key=False, default=date.today)
    model_prediction = Column(Integer,
                              primary_key=False,
                              index=True,
                              default=1
                              )  # Remove the default value when model deployed
