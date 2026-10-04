from fastapi import FastAPI
from pydantic import BaseModel,Field,EmailStr

app=FastAPI()

class userDetails(BaseModel): #Creating Class to get info about user
    First_Name:str=Field(...,min_length=3,max_length=10)

    Last_Name:str=Field(...,min_length=3,max_length=10)

    UserName:str=Field(...,min_length=4,max_lentgh=15)

    Mobile_No:int=Field(...,ge=10)

    Email:str

    Password:str=Field(...,min_length=4,max_length=8)


class Profile(BaseModel):#Create a response class
    First_Name:str

    Last_Name:str

    UserName:str


@app.post("/Profile",response_model=Profile)

def UserProfile(User:userDetails):
    #Returns all objects in User
    #But FastAPI will filter sensitive data automatically
    return User