from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base, Comment

class Company(Base):
    __tablename__ = 'company'

    id = Column("pk_company", Integer, primary_key=True)
    company_name = Column(String(140), unique=True)
    trading_name = Column(String(140))
    cnpj = Column(String(18))
    contact_name = Column(String(100))
    phone = Column(String(15))
    email = Column(String(100))
    insertion_date = Column(DateTime, default=datetime.now())

    """ Definition of the relationship between the company and the comment.
    The relationship is implicit and not saved in the 'company' table, it is SQLAlchemy's responsibility to reconstruct this relationship."""
    comments = relationship("Comment")

    def __init__(self, company_name:str, trading_name:str, cnpj:str, contact_name:str, phone:str, email:str,
                 insertion_date:Union[DateTime, None] = None):
        """ Creates a company

        Arguments:
            *company_name: name of the company.
            *trading_name: trading name of the company.
            *cnpj: CNPJ of the company.
            *contact_name: Name of the contact person at the company.
            *phone: Company contact phone number.
            *email: Company contact email.
            *insertion_date: date when the company was inserted into the database.
        """
        self.company_name = company_name
        self.trading_name = trading_name
        self.cnpj = cnpj
        self.contact_name = contact_name
        self.phone = phone
        self.email = email

        # If the date is not provided, it will be the exact date of insertion into the database.
        if insertion_date:
            self.insertion_date = insertion_date

    def add_comment(self, comment:Comment):
        """ Adds a new comment to the company """
        self.comments.append(comment)
