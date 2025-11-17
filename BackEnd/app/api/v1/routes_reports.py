from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.core.security import get_current_user_optional
from app.utils.pdf_generator import generate_animal_traceability_report, generate_compliance_report
from datetime import datetime

router = APIRouter()


@router.get("/animals/{animal_id}/pdf", tags=["Reports"])
async def export_animal_traceability_pdf(
    animal_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_optional)
):
    """
    Generate and download a PDF traceability report for an animal.
    
    - **animal_id**: ID of the animal to generate report for
    
    Returns a PDF file with animal information, movement history, and event timeline.
    """
    # Get animal data
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    # Prepare animal data
    animal_data = {
        "id": animal.id,
        "name": animal.name,
        "tag_id": animal.tag_id,
        "species": animal.species,
        "breed": {
            "name": animal.breed.name if animal.breed else "Unknown"
        },
        "facility": {
            "name": animal.facility.name if animal.facility else "Unknown"
        },
        "owner": {
            "username": animal.owner.username if animal.owner else "Unknown"
        },
        "date_added": str(animal.date_added) if animal.date_added else None
    }
    
    # Get movement history
    movements = db.query(models.Movement).filter(
        models.Movement.animal_id == animal_id
    ).order_by(models.Movement.timestamp.desc()).all()
    
    movement_data = []
    for movement in movements:
        facility = db.query(models.Facility).filter(
            models.Facility.id == movement.facility_id
        ).first()
        movement_data.append({
            "facility_name": facility.name if facility else "Unknown",
            "facility_type": facility.facility_type if facility else "Unknown",
            "facility_location": facility.location if facility else "Unknown",
            "timestamp": str(movement.timestamp)
        })
    
    # Get event history
    events = db.query(models.Event).filter(
        models.Event.animal_id == animal_id
    ).order_by(models.Event.timestamp.desc()).all()
    
    event_data = []
    for event in events:
        event_data.append({
            "timestamp": str(event.timestamp),
            "event_type": event.event_type,
            "is_valid": event.is_valid,
            "event_metadata": event.event_metadata or "No details"
        })
    
    # Generate PDF
    pdf_buffer = generate_animal_traceability_report(animal_data, event_data, movement_data)
    
    # Create filename
    filename = f"animal_{animal_id}_traceability_report_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    # Return PDF as streaming response
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/compliance/pdf", tags=["Reports"])
async def export_compliance_pdf(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_optional)
):
    """
    Generate and download a compliance report PDF (regulator access only).
    
    Returns a PDF file with system statistics, anomalies, and facility information.
    """
    # Check if user is a regulator
    if current_user.role != "regulator":
        raise HTTPException(status_code=403, detail="Access denied. Regulator role required.")
    
    # Get system statistics
    total_animals = db.query(models.Animal).count()
    total_events = db.query(models.Event).count()
    anomalies_count = db.query(models.Event).filter(models.Event.is_valid == False).count()
    total_facilities = db.query(models.Facility).count()
    
    stats = {
        "totalAnimals": total_animals,
        "totalEvents": total_events,
        "anomalies": anomalies_count,
        "totalFacilities": total_facilities
    }
    
    # Get recent anomalies
    anomalies = db.query(models.Event).filter(
        models.Event.is_valid == False
    ).order_by(models.Event.timestamp.desc()).limit(50).all()
    
    anomaly_data = []
    for anomaly in anomalies:
        anomaly_data.append({
            "timestamp": str(anomaly.timestamp),
            "animal_id": anomaly.animal_id,
            "event_type": anomaly.event_type,
            "anomaly_reason": getattr(anomaly, 'anomaly_reason', 'Validation failed')
        })
    
    # Get facilities
    facilities = db.query(models.Facility).all()
    
    facility_data = []
    for facility in facilities:
        facility_data.append({
            "name": facility.name,
            "facility_type": facility.facility_type,
            "location": facility.location
        })
    
    # Generate PDF
    pdf_buffer = generate_compliance_report(stats, anomaly_data, facility_data)
    
    # Create filename
    filename = f"compliance_report_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    # Return PDF as streaming response
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/audit-logs/pdf", tags=["Reports"])
async def export_audit_logs_pdf(
    request: Request,
    event_type: str = None,
    validity: str = None,
    facility_id: int = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_optional)
):
    """
    Generate and download an audit log report PDF with filters.
    
    - **event_type**: Filter by event type (optional)
    - **validity**: Filter by validity: "valid", "anomaly", or "all" (optional)
    - **facility_id**: Filter by facility ID (optional)
    
    Returns a PDF file with filtered audit logs.
    """
    # Check if user is a regulator
    if current_user.role != "regulator":
        raise HTTPException(status_code=403, detail="Access denied. Regulator role required.")
    
    # Build query
    query = db.query(models.Event)
    
    if event_type:
        query = query.filter(models.Event.event_type == event_type)
    
    if validity == "valid":
        query = query.filter(models.Event.is_valid == True)
    elif validity == "anomaly":
        query = query.filter(models.Event.is_valid == False)
    
    if facility_id:
        query = query.filter(models.Event.facility_id == facility_id)
    
    events = query.order_by(models.Event.timestamp.desc()).limit(100).all()
    
    # Prepare event data
    event_data = []
    for event in events:
        animal = db.query(models.Animal).filter(models.Animal.id == event.animal_id).first()
        facility = db.query(models.Facility).filter(models.Facility.id == event.facility_id).first()
        
        event_data.append({
            "timestamp": str(event.timestamp),
            "animal_id": event.animal_id,
            "animal_name": animal.name if animal else "Unknown",
            "event_type": event.event_type,
            "facility_name": facility.name if facility else "Unknown",
            "is_valid": event.is_valid,
            "event_metadata": event.event_metadata or "No details"
        })
    
    # Use compliance report generator with event data as anomalies
    stats = {
        "totalAnimals": db.query(models.Animal).count(),
        "totalEvents": len(events),
        "anomalies": sum(1 for e in events if not e.is_valid),
        "totalFacilities": db.query(models.Facility).count()
    }
    
    # Generate PDF (reuse compliance report format)
    pdf_buffer = generate_compliance_report(stats, event_data, [])
    
    # Create filename
    filename = f"audit_logs_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    # Return PDF as streaming response
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
