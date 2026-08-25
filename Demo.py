from fastapi import FastAPI

app=FastAPI()

@app.get("/healthy")

def health_check():
    return {
       "Status":"healthy",
       "service": "auth-backend",
       "active": True 
    }

@app.get("/logs/{log_id}")

def User_id(User_log_id:int):
    return {"User id":{User_log_id},"Status":"GOOD"}
    
