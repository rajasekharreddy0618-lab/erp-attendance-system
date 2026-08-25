from fastapi import FastAPI
from pydantic import BaseModel,Field

app=FastAPI()

class ItemList(BaseModel):
    Item_Name:str=Field(...,min_length=3,max_length=20)
    No_of_item:int=Field(...,gt=0)

class product_list(BaseModel):
    Customer_Name:str=Field(...,min_length=4,max_length=20)
    Total_Items:list[ItemList]

@app.post("/add-items")
def add_items(Info:product_list):
    return{"status":"Data Added successfully",
           "Products Taken":Info,
           "Total items":len(Info.Total_Items)}