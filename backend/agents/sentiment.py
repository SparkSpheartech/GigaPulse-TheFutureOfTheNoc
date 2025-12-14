from sqlalchemy.orm import Session
import models

def analyze_sentiment(db: Session):
    """
    Simulates a Sentiment AI Agent that analyzes customer interactions.
    """
    interactions = db.query(models.CustomerInteraction).all()
    analysis = []
    
    for i in interactions:
        sentiment = "Neutral"
        if i.nps <= 6: sentiment = "Negative"
        if i.nps >= 9: sentiment = "Positive"
        
        analysis.append({
            "interaction_id": i.id,
            "customer_id": i.customer_id,
            "sentiment_score": i.nps,
            "sentiment_label": sentiment,
            "churn_risk": "High" if sentiment == "Negative" else "Low"
        })
        
    return analysis
