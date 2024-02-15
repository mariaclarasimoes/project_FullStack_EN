from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from model import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    text = Column(String(4000))
    insertion_date = Column(DateTime, default=datetime.now())

    """Definition of the relationship between the comment and a company.
    The 'company' column will store the reference to the company, the foreign key that relates a company to the comment."""
    company = Column(Integer, ForeignKey("company.pk_company"), nullable=False)

    def __init__(self, text:str, insertion_date:Union[DateTime, None] = None):
        """Creates a Comment
        Arguments:
            * Text: the text of a comment.
            * Insertion_date: the date when the comment was made or inserted into the database."""
        self.text = text
        if insertion_date:
            self.insertion_date = insertion_date
