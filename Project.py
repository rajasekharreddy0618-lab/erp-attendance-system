from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

#--Define database (sqlite3) filename--
Database="Raju.db"

conn=sqlite3.connect(Database)

cursor=conn.cursor()

#Database setup and start up
cursor.execute("""
               CREATE TABLE IF NOT EXISTS Credit(
               Customer_Name TEXT NOT NULL,
               Product_Name TEXT NOT NULL,
               Quantity INTEGER,
               Unit_Prize FLOAT,
               Total_List FLOAT,
               Total_Bill FLOAT)
               """)

conn.commit()
conn.close()

app=FastAPI(title="SHOP CreditTrack")


#_-_-_-_CORS CONFIGURATION_-_-_-_-
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#_-_-_-_-_PYDANTIC MODELS_-_-_-_-_-
class product_list(BaseModel):
    product_Name:str=Field(...,min_length=4,max_length=20)
    Quantity:int=Field(...,gt=0)
    Unit_prize:float=Field(...,gt=0)


class Deatils(BaseModel):
    Customer_Name:str=Field(...,min_length=4,max_length=15)
    Total_List:list[product_list]


#-----POST ENDPOINT :Calculating bill
@app.post("/Calculate_Bill")
def Calculate_Bill(info:Deatils):
    grand_total = 0.0
    for data in info.Total_List:
        grand_total+=data.Unit_prize*data.Quantity
    grand_total=round(grand_total,2)
    Purchased_items = []
    try:
        conn=sqlite3.connect(Database)
        cursor=conn.cursor()

        for data in info.Total_List:
            item_total = round(data.Unit_prize * data.Quantity, 2)
            

            cursor.execute("""
                       INSERT INTO Credit(Customer_Name,Product_Name,Quantity,Unit_Prize,Total_List,Total_Bill) VALUES(?,?,?,?,?,?)""",
                       (
                           info.Customer_Name,
                           data.product_Name,
                           data.Quantity,
                           data.Unit_prize,
                           item_total,
                           grand_total,
                       ),
                    )
            Purchased_items.append(
                {
                    "Product Name":data.product_Name,
                    "Quantity":data.Quantity,
                    "Unit prize":data.Unit_prize,
                    "Item Total":item_total,
        }
        )
        conn.commit()
        conn.close()
        
        return{
            "Message":"-_-_-_-CREDIT LIST-_-_-_-",
            "Customer Name":info.Customer_Name,
            "Product Name":data.product_Name,
            "Quantity":data.Quantity,
            "Total product list":Purchased_items,
            "Total bill":grand_total,
         }

        
    except Exception as e:
        raise HTTPException(
            status_code=500,detail=f"Database ERROR:{str(e)}"
        )
    
#------GET ENDPOINT ---------
@app.get("/Get_all_credits")
def Get_all_credits():
    try:
        conn=sqlite3.connect(Database)
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM Credit")

        rows=cursor.fetchall()
        conn.close()

        if not rows:
            return{"MESSAGE":"Details not found in database"}
        
        all_records=[]

        for row in rows:
            Customer_Name,product_Name,Quantity,Unit_Prize,Total_list,Total_Bill=(row)
            all_records.append(
    {
        "Customer_Name": Customer_Name,
        "Product_Name": product_Name,  # Ensure this matches exactly
        "Quantity": Quantity,
        "Unit Prize": Unit_Prize,
        "Total Bill": Total_Bill,
    }
)

        return {
            "Total_Entries":len(all_records),
            "All crdeits":all_records,

        }
    except Exception as e:
        raise HTTPException(
            status_code=500,detail=f"Database error:{str(e)}"
        )
    
#----DELETE ENDPOINT--------
@app.delete("/Clear_Credit/{Customer_Name}")
def Clear_Credit(Customer_Name:str):
    try:
        conn=sqlite3.connect(Database)
        cursor=conn.cursor()

        cursor.execute(
            "SELECT * FROM Credit WHERE Customer_Name = ?",(Customer_Name,)
        )

        existing_data=cursor.fetchall()

        if not existing_data:
            conn.close()
            return{"Message":f"No recors found for Customer:{Customer_Name}"}
        

        cursor.execute(
            "DELETE FROM Credit WHERE Customer_Name=?",(Customer_Name,)
        )

        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        if deleted_count==0:
            return{
                "Message":f"No records found matching customer:{Customer_Name}"
            }

        return{"Message":f"Successfully deleted {deleted_count} for Customer:{Customer_Name}"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,detail=f"Database error:{str(e)}"
        )

