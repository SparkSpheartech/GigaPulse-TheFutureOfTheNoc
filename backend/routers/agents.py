from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from agents import topology, diagnostic, sentiment

router = APIRouter()

@router.get("/topology/scan")
def scan_topology(db: Session = Depends(get_db)):
    return topology.analyze_topology(db)

@router.get("/diagnostic/{outage_id}")
def diagnose_outage(outage_id: str, db: Session = Depends(get_db)):
    return diagnostic.run_diagnostics(db, outage_id)

@router.get("/sentiment/analyze")
def analyze_cx(db: Session = Depends(get_db)):
    return sentiment.analyze_sentiment(db)
