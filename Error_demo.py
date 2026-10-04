from fastapi import FastAPI,HTTPException

app=FastAPI()



user={1:"Raju",2:"Kishan"}

@app.get("/user/{user_id}")
def get_user(user_id:int):
    if user_id not in user:
        raise HTTPException(status_code=404,detail="User not found")
    return{"User_id":{user_id},"Name":user[user_id]}
