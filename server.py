import os
from fastapi import FastAPI, HTTPException,Depends,status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine,Column,String
from sqlalchemy.orm import sessionmaker,Session,declarative_base

#Database connection and engine connection
DEFAULT_LOCAL_DB = "postgresql+psycopg2://postgres:raju0618@localhost:5432/raju_db"
db_url = os.getenv("DATABASE_URL", DEFAULT_LOCAL_DB)

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+psycopg2://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
engine=create_engine(db_url)
sessionlocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base=declarative_base()

#database model 
class Attendance(Base):
    __tablename__="attendance"
    USN=Column(String,primary_key=True,index=True)
    Name=Column(String,nullable=False)
    status=Column(String,default="Absent",nullable=False)

#Create table
Base.metadata.create_all(bind=engine)

#Data Dependency  to get database session
def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

        

app = FastAPI(title="ERP 📊")

#Pydantic schema for valadation
class Student(BaseModel):
    USN: str = Field(min_length=9, max_length=10)
    Name: str = Field(max_length=25)

    class Config:
        from_attributes=True

class StudentUpdate(BaseModel):
    Name:str=Field(max_length=25)

class MarkAttendence(BaseModel):
    status:str=Field(...,description="Must be 'Present' or 'Absent'")




# 1.API endpionts to greet
@app.get("/")
def greet():
    return {"message": "Welcome back to FastAPI"}

# 2.API endpoint to get all students data
@app.get("/students")
def get_all_students(db:Session=Depends(get_db)):
    return db.query(Attendance).all()

# 3.PI endpoints to post student data
@app.post("/student",status_code=status.HTTP_201_CREATED)
def post_student(student_data:Student, db:Session=Depends(get_db)):
   existing=db.query(Attendance).filter(Attendance.USN==student_data.USN).first()
   if existing:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        details=f"Student with USN {student_data.USN} already exist"
    ) 
   new_student=Attendance(USN=student_data.USN,Name=student_data.Name,status="Absent")
   db.add(new_student)
   db.commit()
   db.refresh(new_student)
   return new_student

# 4.API endpoints to get student data by usn
@app.get("/student/{USN}")
def get_student(USN:str,db:Session=Depends(get_db)):
    student=db.query(Attendance).filter(Attendance.USN==USN).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="student not found")
    return student

#5.API endpoint to mark attendence
@app.put("/attendance/{USN}")
def markattendence(USN:str,attendence_data:MarkAttendence,db:Session=Depends(get_db)):
    Updated_status=attendence_data.status.capitalize()
    if Updated_status not in ["Present","Absent"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Status must be 'Present' or 'Absent'")
    
    student=db.query(Attendance).filter(Attendance.USN==USN).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="student not found")
    
    student.status=Updated_status
    db.commit()
    db.refresh(student)
    return{"Message":f"Status updated to {Updated_status}","student":student}


# 6.API endpoint to update student data
@app.put("/student/{USN}")
def update_student(USN: str,update_data:StudentUpdate,db:Session=Depends(get_db)):
    student=db.query(Attendance).filter(Attendance.USN==USN).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
    
    student.Name=update_data.Name
    db.commit()
    db.refresh(student)
    return{"Message":"Updated successfully","student":student}

# 7.API endpoint to delete student data
@app.delete("/student/{USN}")
def delete_student(USN: str,db:Session=Depends(get_db)):
    student=db.query(Attendance).filter(Attendance.USN==USN).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
    db.delete(student)
    db.commit()
    return{"Message":"Deleted successfully"}