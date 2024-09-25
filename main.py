from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from get_response import inference


# Create an instance of the FastAPI class
app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # List of allowed origins
    allow_credentials=True,  # Allows cookies and other credentials
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

spa_path = "./web"

class Q(BaseModel):
    query: str


# Define a route
@app.post("/api/ask")
def read_root(q: Q):
    return inference(q.query)


app.mount("/", StaticFiles(directory=spa_path, html=True), name="spa")
