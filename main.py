from fastapi import FastAPI
from pydantic import BaseModel

from get_response import inference


# Create an instance of the FastAPI class
app = FastAPI()

class Q(BaseModel):
    query: str


# Define a route
@app.post("/")
def read_root(q: Q):
    return inference(q.query)
