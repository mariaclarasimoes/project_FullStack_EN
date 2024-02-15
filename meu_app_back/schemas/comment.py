from pydantic import BaseModel


class CommentSchema(BaseModel):
    # Defines how a new comment to be inserted should be represented
    
    company_id: int = 1
    text: str = "Only buy if the price is really good!"
