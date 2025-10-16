from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # farmer, processor, regulator
    animals = relationship("Animal", back_populates="owner", cascade="all, delete-orphan")

class Facility(Base):
    __tablename__ = "facilities"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    facility_type = Column(String)  # farm, processor, retailer

class Animal(Base):
    __tablename__ = "animals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    tag_id = Column(String, unique=True)
    date_added = Column(DateTime)
    facility_id = Column(Integer, ForeignKey("facilities.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    facility = relationship("Facility")
    owner = relationship("User", back_populates="animals")
    events = relationship("Event", back_populates="animal", cascade="all, delete-orphan")

class AnimalBreed(Base):
    __tablename__ = "animal_breeds"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100))
    iso3 = Column(String(3))
    specie = Column(String(100))
    breed_name = Column(String(150))
    language = Column(String(50))
    description = Column(Text)
    transboundary_name = Column(String(150))
    other_name = Column(String(150))

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    event_type = Column(String)
    actor_id = Column(Integer, ForeignKey("users.id"))
    facility_id = Column(Integer, ForeignKey("facilities.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_metadata = Column(String)
    is_valid = Column(Boolean, default=True)
    anomaly_reason = Column(String, nullable=True)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    animal = relationship("Animal", back_populates="events")