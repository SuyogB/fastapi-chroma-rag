# Define a model for the FastAPI application

from pydantic import BaseModel

class Query(BaseModel):
    query: str # The search query input by the user
    neighbours: int = 3 # Number of similar items to retrieve, default is 3