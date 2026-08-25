from fastapi import FastAPI
from pydantic import BaseModel,Field
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
origins = [
    "http://localhost:3000",       # React default port
    "http://localhost:8000",       #backend default port
    "http://127.0.0.1:5500",       # VS Code Live Server
    # "*"                          # Use "*" to allow all origins during local testing
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Whitelist specific domains or use ["*"]
    allow_credentials=True,  #All cookies 
    allow_methods=["*"],     #POST GET(All HTTP requests)
    allow_headers=["*"]  #Allow All HTTP headers
)

@app.get("/root")
def root():
    return{"Message":"CORS configured successfully"}
