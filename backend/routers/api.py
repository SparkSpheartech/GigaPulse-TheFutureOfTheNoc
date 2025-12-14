from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/outages")
def get_outages(db: Session = Depends(get_db)):
    return db.query(models.OutageEvent).all()

@router.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()

@router.get("/infrastructure")
def get_infrastructure(db: Session = Depends(get_db)):
    return db.query(models.Infrastructure).all()
