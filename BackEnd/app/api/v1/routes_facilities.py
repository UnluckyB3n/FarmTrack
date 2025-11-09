from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional

from app.db.session import get_db
from app.db.models import Facility, Animal, Event

router = APIRouter()


@router.post("/", status_code=201)
def create_facility(payload: dict, db: Session = Depends(get_db)):
    """Create a new facility. Expects keys: name, location, facility_type"""
    name = payload.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Facility name is required")

    facility = Facility(name=name, location=payload.get("location"), facility_type=payload.get("facility_type"))
    db.add(facility)
    db.commit()
    db.refresh(facility)

    return {"status": "success", "facility": {"id": facility.id, "name": facility.name, "location": facility.location, "facility_type": facility.facility_type}}


@router.get("/")
def list_facilities(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    facility_type: Optional[str] = None,
    location: Optional[str] = None,
    search: Optional[str] = None
):
    """List facilities with filtering, search, and pagination"""
    query = db.query(Facility)
    
    if facility_type:
        query = query.filter(Facility.facility_type == facility_type)
    if location:
        query = query.filter(Facility.location.ilike(f"%{location}%"))
    if search:
        query = query.filter(
            or_(
                Facility.name.ilike(f"%{search}%"),
                Facility.location.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    facilities = query.offset(skip).limit(limit).all()
    
    result = []
    for f in facilities:
        result.append({"id": f.id, "name": f.name, "location": f.location, "facility_type": f.facility_type})
    return {"facilities": result, "total": total, "skip": skip, "limit": limit}


@router.get("/{facility_id}")
def get_facility(facility_id: int, db: Session = Depends(get_db)):
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    return {"id": facility.id, "name": facility.name, "location": facility.location, "facility_type": facility.facility_type}


@router.put("/{facility_id}")
def update_facility(facility_id: int, payload: dict, db: Session = Depends(get_db)):
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")

    if "name" in payload:
        facility.name = payload.get("name")
    if "location" in payload:
        facility.location = payload.get("location")
    if "facility_type" in payload:
        facility.facility_type = payload.get("facility_type")

    db.add(facility)
    db.commit()
    db.refresh(facility)

    return {"status": "success", "facility": {"id": facility.id, "name": facility.name, "location": facility.location, "facility_type": facility.facility_type}}


@router.delete("/{facility_id}")
def delete_facility(facility_id: int, db: Session = Depends(get_db)):
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")

    db.delete(facility)
    db.commit()

    return {"status": "deleted"}

@router.get("/types")
def list_facility_types(db: Session = Depends(get_db)):
    """Get distinct list of all facility types"""
    types = db.query(Facility.facility_type).distinct().all()
    return {"facility_types": [t[0] for t in types if t[0]]}

@router.get("/{facility_id}/animals")
def get_facility_animals(
    facility_id: int,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all animals at a specific facility"""
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    
    query = db.query(Animal).filter(Animal.facility_id == facility_id)
    total = query.count()
    animals = query.offset(skip).limit(limit).all()
    
    result = []
    for a in animals:
        result.append({
            "id": a.id,
            "name": a.name,
            "species": a.species,
            "tag_id": a.tag_id,
            "date_added": str(a.date_added) if a.date_added else None
        })
    
    return {
        "facility": {
            "id": facility.id,
            "name": facility.name,
            "location": facility.location,
            "facility_type": facility.facility_type
        },
        "animals": result,
        "total": total
    }

@router.get("/{facility_id}/stats")
def get_facility_stats(facility_id: int, db: Session = Depends(get_db)):
    """Get statistics for a specific facility"""
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    
    animal_count = db.query(func.count(Animal.id)).filter(Animal.facility_id == facility_id).scalar()
    event_count = db.query(func.count(Event.id)).filter(Event.facility_id == facility_id).scalar()
    
    animals_by_species = db.query(
        Animal.species,
        func.count(Animal.id)
    ).filter(Animal.facility_id == facility_id).group_by(Animal.species).all()
    
    return {
        "facility": {
            "id": facility.id,
            "name": facility.name,
            "location": facility.location,
            "facility_type": facility.facility_type
        },
        "total_animals": animal_count,
        "total_events": event_count,
        "animals_by_species": [{"species": s, "count": c} for s, c in animals_by_species]
    }
