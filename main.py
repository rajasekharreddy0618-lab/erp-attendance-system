from fastapi import FastAPI

# Initialize the app instance
app = FastAPI()

# Decorator: Map an HTTP GET request on the root route "/" to a function
@app.get("/")
def read_root():
    return {"message": "Welcome to the Backend API!", "status": "online"}

# Path Parameter Example: Fetching a specific item by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "role": "Standard User"}