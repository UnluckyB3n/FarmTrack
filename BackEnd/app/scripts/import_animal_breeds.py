import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import AnimalBreed
from app.db.base import Base

DATABASE_URL = "postgresql://postgres:postgres@db:5432/traceability"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

with open("app/data/animal_breeds.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        breed = AnimalBreed(
            country=row.get("Country"),
            iso3=row.get("ISO3"),
            specie=row.get("Specie"),
            breed_name=row.get("Breed/Most common name"),
            language=row.get("Language"),
            description=row.get("Description"),
            transboundary_name=row.get("Transboundary name"),
            other_name=row.get("Other name")
        )
        session.add(breed)

session.commit()
print("✅ CSV import complete!")
