from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Facility

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
def list_facilities(db: Session = Depends(get_db)):
    facilities = db.query(Facility).all()
    result = []
    for f in facilities:
        result.append({"id": f.id, "name": f.name, "location": f.location, "facility_type": f.facility_type})
    return {"facilities": result}


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
