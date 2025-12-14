from sqlalchemy.orm import Session
import models

def analyze_topology(db: Session):
    """
    Simulates a Topology AI Agent that scans infrastructure and detects missing links or redundancy gaps.
    """
    infra = db.query(models.Infrastructure).all()
    results = []
    
    for item in infra:
        if item.status == "DAMAGED":
            results.append({
                "id": item.id,
                "issue": "Critical Link Failure",
                "impact": "High - No Redundancy Detected",
                "recommendation": "Reroute traffic via Backup Trunk B01"
            })
            
    return results
