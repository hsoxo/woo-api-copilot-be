from fastapi import FastAPI

from get_response import inference


# Create an instance of the FastAPI class
app = FastAPI()



# Define a route
@app.get("/")
def read_root():
    return inference("How to get the user profile")
