from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import engine, get_db
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Doctor Service")


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    experience: int
    available: bool = True


@app.get("/")
def home():
    return {"message": "Doctor Service is running"}


@app.post("/doctors")
def add_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):

    new_doctor = models.Doctor(
        **doctor.model_dump()
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


@app.get("/doctors")
def get_doctors(db: Session = Depends(get_db)):

    return db.query(models.Doctor).all()


@app.get("/doctors/{doctor_id}")
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    doctor = db.query(models.Doctor).filter(
        models.Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@app.patch("/doctors/{doctor_id}/availability")
def update_availability(
    doctor_id: int,
    available: bool,
    db: Session = Depends(get_db)
):

    doctor = db.query(models.Doctor).filter(
        models.Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.available = available

    db.commit()

    return {"message": "Availability updated"}