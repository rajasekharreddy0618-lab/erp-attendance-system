from fastapi import FastAPI
from pydantic import BaseModel,Field

app=FastAPI()

class Product_Details(BaseModel):
    Item_Name:str=Field(...,min_length=3,max_length=20)
    Quantity:int=Field(...,gt=0)
    Price_per_unit:float=Field(...,gt=0)

class Product_list(BaseModel):
    Customer_Name:str=Field(...,min_length=4,max_length=10)
    Total_list:list[Product_Details]


@app.post("/Calculate_bill")
def Calculate_bill(Data:Product_list):
    Grand_Total=0.0

    for items in Data.Total_list:
        Grand_Total+=items.Quantity*items.Price_per_unit
    Grand_Total=round(Grand_Total,2)
    return{
        "--Customer Debit Details--"
        "Customer Name":Data.Customer_Name,
        "Product List":Data.Total_list,
        "Total Quantity":len(Data.Total_list),
        "Total Bill":Grand_Total
    }