from fastapi import FastAPI,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer

app=FastAPI()

oauthr_scheme=OAuth2PasswordBearer(tokenUrl="login")

access_token="Wirstband0618"
@app.post("/login")
def login():
    return{"Access_token":access_token}

@app.get("/Dashboard")
def dashboard(Token:str=Depends(oauthr_scheme)):
    if Token!=access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED ACCESS"
        )
    return{"Message":"Permission Granted"}