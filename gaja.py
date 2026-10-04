from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# 1. Database Connection & Engine Setup
DB_URL = "postgresql+psycopg2://postgres:raju0618@localhost:5432/raju_db"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 2. Database Model
class Attendance(Base):
    __tablename__ = "attendance"

    USN = Column(String, primary_key=True, index=True)
    Name = Column(String, nullable=False)


# 3. Create Table
Base.metadata.create_all(bind=engine)


# 4. Dependency to Get Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 5. FastAPI App & Request Schema
app = FastAPI(title="ERP Attendance API")


class AttendanceCreate(BaseModel):
    USN: str
    Name: str


# 6. API Endpoints for Inserting and Reading Data

@app.post("/attendance")
def add_student(student: AttendanceCreate, db: Session = Depends(get_db)):
    # Assign and save data to database
    record = Attendance(USN=student.USN, Name=student.Name)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"status": "success", "data": {"USN": record.USN, "Name": record.Name}}


@app.get("/attendance")
def get_all_students(db: Session = Depends(get_db)):
    # Retrieve all records from database
    return db.query(Attendance).all()