from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional
from app.db.session import get_db
from app.db.models import Animal, AnimalBreed, Event, Facility, User
from app.utils.qr_generator import generate_qr_response, generate_animal_qr_url

router = APIRouter()

# --- Animal Breeds Endpoints (must be BEFORE /{animal_id} routes!) ---

@router.get("/breeds")
def list_animal_breeds(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=10000),
    species: Optional[str] = None,
    country: Optional[str] = None,
    search: Optional[str] = None
):
    """List animal breeds with optional filtering, search, and pagination"""
    query = db.query(AnimalBreed)
    
    if species:
        query = query.filter(AnimalBreed.specie.ilike(f"%{species}%"))
    if country:
        query = query.filter(AnimalBreed.country.ilike(f"%{country}%"))
    if search:
        query = query.filter(
            or_(
                AnimalBreed.breed_name.ilike(f"%{search}%"),
                AnimalBreed.description.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    breeds = query.offset(skip).limit(limit).all()
    
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
    return {"breeds": result, "total": total, "skip": skip, "limit": limit}

@router.get("/breeds/{breed_id}")
def get_animal_breed(breed_id: int, db: Session = Depends(get_db)):
    """Get a specific animal breed by ID"""
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

@router.get("/species")
def list_species(db: Session = Depends(get_db)):
    """Get distinct list of all animal species"""
    species = db.query(Animal.species).distinct().all()
    return {"species": [s[0] for s in species if s[0]]}

@router.get("/stats")
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

# --- Animal Endpoints ---

@router.post("/", status_code=201)
def create_animal(payload: dict, db: Session = Depends(get_db)):
    """Create a new animal. Expects keys: name, species, breed_id, tag_id, date_added, facility_id, owner_id"""
    name = payload.get("name")
    species = payload.get("species")
    if not name or not species:
        raise HTTPException(status_code=400, detail="Animal name and species are required")

    animal = Animal(
        name=name,
        species=species,
        breed_id=payload.get("breed_id"),
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
    
    # Build breed data if available
    breed_data = None
    if animal.breed_id and animal.breed:
        breed_data = {
            "id": animal.breed.id,
            "name": animal.breed.breed_name,
            "code": animal.breed.iso3,
            "country": animal.breed.country,
            "description": animal.breed.description
        }
    
    # Build facility data if available
    facility_data = None
    if animal.facility_id and animal.facility:
        facility_data = {
            "id": animal.facility.id,
            "name": animal.facility.name,
            "facility_type": animal.facility.facility_type,
            "location": animal.facility.location
        }
    
    # Build owner data if available
    owner_data = None
    if animal.owner_id and animal.owner:
        owner_data = {
            "id": animal.owner.id,
            "username": animal.owner.username
        }
    
    return {
        "id": animal.id,
        "name": animal.name,
        "species": animal.species,
        "breed_id": animal.breed_id,
        "breed": breed_data,
        "tag_id": animal.tag_id,
        "date_added": str(animal.date_added) if animal.date_added else None,
        "facility_id": animal.facility_id,
        "facility": facility_data,
        "owner_id": animal.owner_id,
        "owner": owner_data
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
    if "breed_id" in payload:
        animal.breed_id = payload.get("breed_id")
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
            "breed_id": animal.breed_id,
            "tag_id": animal.tag_id,
            "date_added": str(animal.date_added) if animal.date_added else None,
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


@router.get("/{animal_id}/qr")
def get_animal_qr_code(animal_id: int, db: Session = Depends(get_db)):
    """
    Generate QR code for animal public tracking page.
    Returns a PNG image that can be scanned to view animal traceability.
    """
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    # Generate public tracking URL
    tracking_url = generate_animal_qr_url(animal_id)
    
    # Return QR code image
    return generate_qr_response(tracking_url)


@router.get("/{animal_id}/tracking-url")
def get_animal_tracking_url(animal_id: int, db: Session = Depends(get_db)):
    """
    Get the public tracking URL for an animal.
    """
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    tracking_url = generate_animal_qr_url(animal_id)
    
    return {
        "animal_id": animal_id,
        "tracking_url": tracking_url,
        "qr_code_url": f"/api/v1/animals/{animal_id}/qr"
    }


@router.post("/{animal_id}/transfer")
def transfer_animal(
    animal_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    """
    Transfer an animal to a new facility.
    Creates a 'movement' event and updates the animal's facility_id.
    
    Payload:
    - to_facility_id: ID of the destination facility
    - actor_id: ID of the user performing the transfer
    - notes: Optional notes about the transfer
    """
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    to_facility_id = payload.get("to_facility_id")
    actor_id = payload.get("actor_id")
    notes = payload.get("notes", "")
    
    if not to_facility_id:
        raise HTTPException(status_code=400, detail="to_facility_id is required")
    
    # Check if destination facility exists
    to_facility = db.query(Facility).filter(Facility.id == to_facility_id).first()
    if not to_facility:
        raise HTTPException(status_code=404, detail="Destination facility not found")
    
    # Get current facility name for the event metadata
    from_facility = db.query(Facility).filter(Facility.id == animal.facility_id).first() if animal.facility_id else None
    from_facility_name = from_facility.name if from_facility else "Unknown"
    
    # Create movement event
    metadata = f"Transferred from {from_facility_name} to {to_facility.name}"
    if notes:
        metadata += f". Notes: {notes}"
    
    movement_event = Event(
        event_type="movement",
        animal_id=animal_id,
        actor_id=actor_id,
        facility_id=to_facility_id,
        event_metadata=metadata,
        is_valid=True
    )
    
    # Update animal's current facility
    animal.facility_id = to_facility_id
    
    db.add(movement_event)
    db.add(animal)
    db.commit()
    db.refresh(animal)
    db.refresh(movement_event)
    
    return {
        "status": "success",
        "message": f"Animal transferred to {to_facility.name}",
        "animal": {
            "id": animal.id,
            "name": animal.name,
            "facility_id": animal.facility_id,
            "facility_name": to_facility.name
        },
        "event": {
            "id": movement_event.id,
            "event_type": movement_event.event_type,
            "timestamp": str(movement_event.timestamp),
            "metadata": movement_event.event_metadata
        }
    }


@router.get("/{animal_id}/movement-history")
def get_animal_movement_history(animal_id: int, db: Session = Depends(get_db)):
    """
    Get the complete movement history of an animal across facilities.
    Returns all 'movement' events with facility details.
    """
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    # Get all movement events
    movement_events = db.query(Event).filter(
        Event.animal_id == animal_id,
        Event.event_type == "movement"
    ).order_by(Event.timestamp.desc()).all()
    
    result = []
    for event in movement_events:
        facility = db.query(Facility).filter(Facility.id == event.facility_id).first()
        result.append({
            "id": event.id,
            "timestamp": str(event.timestamp),
            "facility_id": event.facility_id,
            "facility_name": facility.name if facility else "Unknown",
            "facility_type": facility.facility_type if facility else None,
            "facility_location": facility.location if facility else None,
            "metadata": event.event_metadata,
            "actor_id": event.actor_id
        })
    
    return {
        "animal": {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,
            "current_facility_id": animal.facility_id
        },
        "movement_history": result,
        "total_movements": len(result)
    }