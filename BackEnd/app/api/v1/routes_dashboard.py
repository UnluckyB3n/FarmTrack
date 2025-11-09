from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from app.db.session import get_db
from app.db.models import Animal, Event, Facility, User

router = APIRouter()

@router.get("/overview")
def get_dashboard_overview(db: Session = Depends(get_db)):
    """Get overall dashboard statistics"""
    total_animals = db.query(func.count(Animal.id)).scalar()
    total_facilities = db.query(func.count(Facility.id)).scalar()
    total_users = db.query(func.count(User.id)).scalar()
    total_events = db.query(func.count(Event.id)).scalar()
    
    # Events in last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_events = db.query(func.count(Event.id)).filter(Event.timestamp >= seven_days_ago).scalar()
    
    # Anomalies
    total_anomalies = db.query(func.count(Event.id)).filter(Event.is_valid == False).scalar()
    recent_anomalies = db.query(func.count(Event.id)).filter(
        Event.is_valid == False,
        Event.timestamp >= seven_days_ago
    ).scalar()
    
    return {
        "totals": {
            "animals": total_animals,
            "facilities": total_facilities,
            "users": total_users,
            "events": total_events
        },
        "recent_activity": {
            "events_last_7_days": recent_events,
            "anomalies_last_7_days": recent_anomalies
        },
        "anomalies": {
            "total": total_anomalies,
            "rate": round(total_anomalies / max(total_events, 1) * 100, 2)
        }
    }

@router.get("/recent-events")
def get_recent_events(db: Session = Depends(get_db), limit: int = 10):
    """Get most recent events with related information"""
    events = db.query(Event).order_by(desc(Event.timestamp)).limit(limit).all()
    
    result = []
    for e in events:
        animal = db.query(Animal).filter(Animal.id == e.animal_id).first()
        facility = db.query(Facility).filter(Facility.id == e.facility_id).first() if e.facility_id else None
        
        result.append({
            "id": e.id,
            "event_type": e.event_type,
            "timestamp": str(e.timestamp),
            "is_valid": e.is_valid,
            "animal": {
                "id": animal.id,
                "name": animal.name,
                "tag_id": animal.tag_id
            } if animal else None,
            "facility": {
                "id": facility.id,
                "name": facility.name
            } if facility else None
        })
    
    return {"events": result}

@router.get("/timeline")
def get_event_timeline(db: Session = Depends(get_db), days: int = 30):
    """Get event counts grouped by day for the last N days"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get events grouped by date
    events_by_day = db.query(
        func.date(Event.timestamp).label('date'),
        func.count(Event.id).label('count'),
        func.sum(func.cast(~Event.is_valid, func.Integer)).label('anomalies')
    ).filter(
        Event.timestamp >= start_date
    ).group_by(
        func.date(Event.timestamp)
    ).order_by('date').all()
    
    timeline = []
    for day in events_by_day:
        timeline.append({
            "date": str(day.date),
            "total_events": day.count,
            "anomalies": day.anomalies or 0
        })
    
    return {"timeline": timeline, "days": days}

@router.get("/top-facilities")
def get_top_facilities(db: Session = Depends(get_db), limit: int = 5):
    """Get facilities with most animals"""
    facilities = db.query(
        Facility.id,
        Facility.name,
        Facility.location,
        Facility.facility_type,
        func.count(Animal.id).label('animal_count')
    ).outerjoin(
        Animal, Animal.facility_id == Facility.id
    ).group_by(
        Facility.id, Facility.name, Facility.location, Facility.facility_type
    ).order_by(
        desc('animal_count')
    ).limit(limit).all()
    
    result = []
    for f in facilities:
        result.append({
            "id": f.id,
            "name": f.name,
            "location": f.location,
            "facility_type": f.facility_type,
            "animal_count": f.animal_count
        })
    
    return {"facilities": result}

@router.get("/species-distribution")
def get_species_distribution(db: Session = Depends(get_db)):
    """Get distribution of animals by species"""
    distribution = db.query(
        Animal.species,
        func.count(Animal.id).label('count')
    ).group_by(Animal.species).order_by(desc('count')).all()
    
    total = sum(d.count for d in distribution)
    
    result = []
    for d in distribution:
        result.append({
            "species": d.species,
            "count": d.count,
            "percentage": round(d.count / max(total, 1) * 100, 2)
        })
    
    return {"distribution": result, "total": total}
