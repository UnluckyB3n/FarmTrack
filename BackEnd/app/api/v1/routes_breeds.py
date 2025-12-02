from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.db.session import get_db
from app.db.models import AnimalBreed

router = APIRouter()


@router.get("/species")
def get_species(db: Session = Depends(get_db)):
    """Get list of all unique species from the breeds database"""
    species = db.query(AnimalBreed.specie).distinct().order_by(AnimalBreed.specie).all()
    return {
        "species": [s[0] for s in species if s[0]]
    }


@router.get("/breeds")
def get_breeds(
    species: Optional[str] = Query(None, description="Filter by species"),
    country: Optional[str] = Query(None, description="Filter by country"),
    search: Optional[str] = Query(None, description="Search in breed name"),
    limit: int = Query(100, ge=1, le=500),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get list of animal breeds with optional filtering"""
    query = db.query(AnimalBreed)
    
    if species:
        query = query.filter(AnimalBreed.specie == species)
    
    if country:
        query = query.filter(AnimalBreed.country == country)
    
    if search:
        query = query.filter(AnimalBreed.breed_name.ilike(f"%{search}%"))
    
    total = query.count()
    breeds = query.order_by(AnimalBreed.breed_name).offset(skip).limit(limit).all()
    
    return {
        "breeds": [
            {
                "id": breed.id,
                "breed_name": breed.breed_name,
                "specie": breed.specie,
                "country": breed.country,
                "iso3": breed.iso3,
                "description": breed.description,
                "transboundary_name": breed.transboundary_name,
                "other_name": breed.other_name,
                "language": breed.language
            }
            for breed in breeds
        ],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/countries")
def get_countries(
    species: Optional[str] = Query(None, description="Filter by species"),
    db: Session = Depends(get_db)
):
    """Get list of countries with breeds, optionally filtered by species"""
    query = db.query(AnimalBreed.country, AnimalBreed.iso3).distinct()
    
    if species:
        query = query.filter(AnimalBreed.specie == species)
    
    countries = query.filter(AnimalBreed.country.isnot(None)).order_by(AnimalBreed.country).all()
    
    return {
        "countries": [
            {"name": c[0], "iso3": c[1]}
            for c in countries if c[0]
        ]
    }


@router.get("/breeds/{breed_id}")
def get_breed_details(breed_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific breed"""
    breed = db.query(AnimalBreed).filter(AnimalBreed.id == breed_id).first()
    
    if not breed:
        return {"error": "Breed not found"}, 404
    
    return {
        "id": breed.id,
        "breed_name": breed.breed_name,
        "specie": breed.specie,
        "country": breed.country,
        "iso3": breed.iso3,
        "description": breed.description,
        "transboundary_name": breed.transboundary_name,
        "other_name": breed.other_name,
        "language": breed.language
    }
