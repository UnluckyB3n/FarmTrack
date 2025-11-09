from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional
from app.db.session import get_db
from app.db.models import Animal, AnimalBreed, Event, Facility, User

router = APIRouter()

# --- Animal Endpoints ---

@router.post("/", status_code=201)
def create_animal(payload: dict, db: Session = Depends(get_db)):
    """Create a new animal. Expects keys: name, species, tag_id, date_added, facility_id, owner_id"""
    name = payload.get("name")
    species = payload.get("species")
    if not name or not species:
        raise HTTPException(status_code=400, detail="Animal name and species are required")

    animal = Animal(
        name=name,
        species=species,
        tag_id=payload.get("tag_id"),
        date_added=payload.get("date_added"),
        facility_id=payload.get("facility_id"),
        owner_id=payload.get("owner_id")
    )
    db.add(animal)
    db.commit()
    db.refresh(animal)

    return {
        "status": "success",
        "animal": {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,
            "tag_id": animal.tag_id,
            "date_added": animal.date_added,
            "facility_id": animal.facility_id,
            "owner_id": animal.owner_id
        }
    }

@router.get("/")
def list_animals(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    species: Optional[str] = None,
    facility_id: Optional[int] = None,
    owner_id: Optional[int] = None,
    search: Optional[str] = None
):
    """List animals with optional filtering, search, and pagination"""
    query = db.query(Animal)
    
    if species:
        query = query.filter(Animal.species.ilike(f"%{species}%"))
    if facility_id:
        query = query.filter(Animal.facility_id == facility_id)
    if owner_id:
        query = query.filter(Animal.owner_id == owner_id)
    if search:
        query = query.filter(
            or_(
                Animal.name.ilike(f"%{search}%"),
                Animal.tag_id.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    animals = query.offset(skip).limit(limit).all()
    
    result = []
    for a in animals:
        result.append({
            "id": a.id,
            "name": a.name,
            "species": a.species,
            "tag_id": a.tag_id,
            "date_added": str(a.date_added) if a.date_added else None,
            "facility_id": a.facility_id,
            "owner_id": a.owner_id
        })
    return {"animals": result, "total": total, "skip": skip, "limit": limit}

@router.get("/{animal_id}")
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return {
        "id": animal.id,
        "name": animal.name,
        "species": animal.species,
        "tag_id": animal.tag_id,
        "date_added": animal.date_added,
        "facility_id": animal.facility_id,
        "owner_id": animal.owner_id
    }

@router.put("/{animal_id}")
def update_animal(animal_id: int, payload: dict, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    if "name" in payload:
        animal.name = payload.get("name")
    if "species" in payload:
        animal.species = payload.get("species")
    if "tag_id" in payload:
        animal.tag_id = payload.get("tag_id")
    if "date_added" in payload:
        animal.date_added = payload.get("date_added")
    if "facility_id" in payload:
        animal.facility_id = payload.get("facility_id")
    if "owner_id" in payload:
        animal.owner_id = payload.get("owner_id")

    db.add(animal)
    db.commit()
    db.refresh(animal)

    return {
        "status": "success",
        "animal": {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,
            "tag_id": animal.tag_id,
            "date_added": animal.date_added,
            "facility_id": animal.facility_id,
            "owner_id": animal.owner_id
        }
    }

@router.delete("/{animal_id}")
def delete_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    db.delete(animal)
    db.commit()

    return {"status": "deleted"}

# --- Animal Breeds Endpoint ---

@router.get("/breeds/")
def list_animal_breeds(db: Session = Depends(get_db)):
    breeds = db.query(AnimalBreed).all()
    result = []
    for b in breeds:
        result.append({
            "id": b.id,
            "country": b.country,
            "iso3": b.iso3,
            "specie": b.specie,
            "breed_name": b.breed_name,
            "language": b.language,
            "description": b.description,
            "transboundary_name": b.transboundary_name,
            "other_name": b.other_name
        })
    return {"breeds": result}
@router.get("/breeds/{breed_id}")
def get_animal_breed(breed_id: int, db: Session = Depends(get_db)):
    breed = db.query(AnimalBreed).filter(AnimalBreed.id == breed_id).first()
    if not breed:
        raise HTTPException(status_code=404, detail="Breed not found")
    return {
        "id": breed.id,
        "country": breed.country,
        "iso3": breed.iso3,
        "specie": breed.specie,
        "breed_name": breed.breed_name,
        "language": breed.language,
        "description": breed.description,
        "transboundary_name": breed.transboundary_name,
        "other_name": breed.other_name
    }

@router.get("/species/")
def list_species(db: Session = Depends(get_db)):
    """Get distinct list of all animal species"""
    species = db.query(Animal.species).distinct().all()
    return {"species": [s[0] for s in species if s[0]]}

@router.get("/stats/")
def get_animal_statistics(db: Session = Depends(get_db)):
    """Get overall animal statistics"""
    total_animals = db.query(func.count(Animal.id)).scalar()
    by_species = db.query(Animal.species, func.count(Animal.id)).group_by(Animal.species).all()
    by_facility = db.query(
        Facility.name,
        func.count(Animal.id)
    ).join(Animal, Animal.facility_id == Facility.id).group_by(Facility.name).all()
    
    return {
        "total_animals": total_animals,
        "by_species": [{"species": s, "count": c} for s, c in by_species],
        "by_facility": [{"facility": f, "count": c} for f, c in by_facility]
    }

@router.get("/{animal_id}/events")
def get_animal_events(animal_id: int, db: Session = Depends(get_db)):
    """Get all events related to a specific animal"""
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    events = db.query(Event).filter(Event.animal_id == animal_id).order_by(Event.timestamp.desc()).all()
    
    result = []
    for e in events:
        result.append({
            "id": e.id,
            "event_type": e.event_type,
            "timestamp": str(e.timestamp),
            "is_valid": e.is_valid,
            "anomaly_reason": e.anomaly_reason,
            "actor_id": e.actor_id,
            "facility_id": e.facility_id,
            "metadata": e.event_metadata
        })
    
    return {
        "animal": {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,
            "tag_id": animal.tag_id
        },
        "events": result,
        "total_events": len(result)
    }       