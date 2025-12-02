"""
Database seeder script to populate FarmTrack with realistic data
Run with: python -m app.db.seed_data
"""
from datetime import datetime, timedelta
import random
import csv
import os
from pathlib import Path
from app.db.session import SessionLocal
from app.db.models import User, Facility, Animal, AnimalBreed, Event
from app.core.security import get_password_hash

def seed_users(db):
    """Create sample users"""
    users_data = [
        {"username": "john_farmer", "role": "farmer", "password": "pass123"},
        {"username": "sarah_farmer", "role": "farmer", "password": "pass123"},
        {"username": "mike_processor", "role": "processor", "password": "pass123"},
        {"username": "emma_processor", "role": "processor", "password": "pass123"},
        {"username": "alice_regulator", "role": "regulator", "password": "pass123"},
        {"username": "bob_regulator", "role": "regulator", "password": "pass123"},
        {"username": "farm_admin", "role": "farmer", "password": "admin123"},
    ]
    
    users = []
    for data in users_data:
        existing = db.query(User).filter(User.username == data["username"]).first()
        if not existing:
            user = User(
                username=data["username"],
                password_hash=get_password_hash(data["password"]),
                role=data["role"]
            )
            db.add(user)
            users.append(user)
            print(f"Created user: {data['username']}")
        else:
            users.append(existing)
            print(f"User already exists: {data['username']}")
    
    db.commit()
    return users

def seed_facilities(db):
    """Create sample facilities"""
    facilities_data = [
        {"name": "Green Valley Farm", "location": "Vermont", "facility_type": "farm"},
        {"name": "Sunny Meadows Ranch", "location": "Texas", "facility_type": "farm"},
        {"name": "Highland Cattle Co", "location": "Scotland", "facility_type": "farm"},
        {"name": "Prairie View Dairy", "location": "Wisconsin", "facility_type": "farm"},
        {"name": "Mountain Peak Livestock", "location": "Colorado", "facility_type": "farm"},
        {"name": "Prime Meats Processing", "location": "Iowa", "facility_type": "processor"},
        {"name": "Quality Dairy Products", "location": "California", "facility_type": "processor"},
        {"name": "Farm Fresh Market", "location": "New York", "facility_type": "retailer"},
        {"name": "Organic Foods Depot", "location": "Oregon", "facility_type": "retailer"},
        {"name": "Local Butcher Shop", "location": "Maine", "facility_type": "retailer"},
    ]
    
    facilities = []
    for data in facilities_data:
        existing = db.query(Facility).filter(Facility.name == data["name"]).first()
        if not existing:
            facility = Facility(**data)
            db.add(facility)
            facilities.append(facility)
            print(f"Created facility: {data['name']}")
        else:
            facilities.append(existing)
            print(f"Facility already exists: {data['name']}")
    
    db.commit()
    return facilities

def seed_animal_breeds(db):
    """Create animal breeds from CSV file"""
    # Get the CSV file path (data folder is at app/data)
    current_dir = Path(__file__).parent.parent  # Go up to app/ directory
    csv_path = current_dir / "data" / "animal_breeds.csv"
    
    if not csv_path.exists():
        print(f"Warning: CSV file not found at {csv_path}")
        print("Skipping breed seeding...")
        return []
    
    breeds = []
    breeds_added = 0
    breeds_skipped = 0
    
    print(f"Loading breeds from: {csv_path}")
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                # Map CSV columns to database fields
                breed_data = {
                    "country": row.get("Country", "").strip(),
                    "iso3": row.get("ISO3", "").strip(),
                    "specie": row.get("Specie", "").strip(),
                    "breed_name": row.get("Breed/Most common name", "").strip(),
                    "language": row.get("Language", "").strip(),
                    "description": row.get("Description", "").strip(),
                    "transboundary_name": row.get("Transboundary name", "").strip(),
                    "other_name": row.get("Other name", "").strip()
                }
                
                # Skip if essential fields are missing
                if not breed_data["breed_name"] or not breed_data["specie"]:
                    continue
                
                # Check if breed already exists
                existing = db.query(AnimalBreed).filter(
                    AnimalBreed.breed_name == breed_data["breed_name"],
                    AnimalBreed.specie == breed_data["specie"],
                    AnimalBreed.country == breed_data["country"]
                ).first()
                
                if not existing:
                    breed = AnimalBreed(**breed_data)
                    db.add(breed)
                    breeds.append(breed)
                    breeds_added += 1
                    
                    # Commit in batches of 100 to improve performance
                    if breeds_added % 100 == 0:
                        db.commit()
                        print(f"  Processed {breeds_added} breeds...")
                else:
                    breeds.append(existing)
                    breeds_skipped += 1
    
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        db.rollback()
        return []
    
    # Final commit
    db.commit()
    print(f"Breed seeding complete: {breeds_added} added, {breeds_skipped} skipped")
    return breeds

def seed_animals(db, facilities, users):
    """Create sample animals"""
    farm_facilities = [f for f in facilities if f.facility_type == "farm"]
    farmer_users = [u for u in users if u.role == "farmer"]
    
    if not farm_facilities or not farmer_users:
        print("Need facilities and users first!")
        return []
    
    species_list = ["Cattle", "Sheep", "Pig", "Goat", "Chicken"]
    cattle_names = ["Bessie", "Daisy", "Buttercup", "Molly", "Belle", "Rosie", "Luna", "Stella", "Ruby", "Pearl"]
    sheep_names = ["Dolly", "Woolly", "Cotton", "Cloud", "Snowball", "Fluffy", "Misty", "Shadow"]
    pig_names = ["Wilbur", "Babe", "Porky", "Hamlet", "Bacon", "Peppa", "Piglet"]
    goat_names = ["Billy", "Gruff", "Nanny", "Capri", "Heidi", "Clover"]
    
    animals = []
    
    # Create 50 animals
    for i in range(50):
        species = random.choice(species_list)
        
        if species == "Cattle":
            name = random.choice(cattle_names)
        elif species == "Sheep":
            name = random.choice(sheep_names)
        elif species == "Pig":
            name = random.choice(pig_names)
        elif species == "Goat":
            name = random.choice(goat_names)
        else:
            name = f"Chicken-{i+1}"
        
        tag_id = f"US{random.randint(100000, 999999)}"
        
        # Check if tag_id exists
        existing = db.query(Animal).filter(Animal.tag_id == tag_id).first()
        if existing:
            continue
        
        animal = Animal(
            name=f"{name}-{random.randint(1, 999)}",
            species=species,
            tag_id=tag_id,
            date_added=datetime.utcnow() - timedelta(days=random.randint(30, 365)),
            facility_id=random.choice(farm_facilities).id,
            owner_id=random.choice(farmer_users).id
        )
        db.add(animal)
        animals.append(animal)
    
    db.commit()
    print(f"Created {len(animals)} animals")
    return animals

def seed_events(db, animals, facilities, users):
    """Create sample events"""
    if not animals:
        print("Need animals first!")
        return []
    
    event_types = [
        "birth", "vaccination", "weighing", "movement", "health_check",
        "feeding", "medication", "breeding", "sale", "slaughter"
    ]
    
    events = []
    
    # Create 200 events
    for _ in range(200):
        animal = random.choice(animals)
        event_type = random.choice(event_types)
        
        # Random timestamp in the last 180 days
        days_ago = random.randint(1, 180)
        timestamp = datetime.utcnow() - timedelta(days=days_ago)
        
        # Randomly mark some events as invalid (anomalies)
        is_valid = random.random() > 0.1  # 10% anomalies
        anomaly_reason = None
        if not is_valid:
            anomaly_reasons = [
                "Weight change too rapid",
                "Event timing inconsistent",
                "Location mismatch",
                "Duplicate event detected",
                "Missing required metadata"
            ]
            anomaly_reason = random.choice(anomaly_reasons)
        
        event = Event(
            event_type=event_type,
            animal_id=animal.id,
            actor_id=random.choice(users).id,
            facility_id=random.choice(facilities).id,
            timestamp=timestamp,
            event_metadata=f"{{\"notes\": \"Sample {event_type} event\"}}",
            is_valid=is_valid,
            anomaly_reason=anomaly_reason
        )
        db.add(event)
        events.append(event)
    
    db.commit()
    print(f"Created {len(events)} events")
    return events

def main():
    """Main seeder function"""
    print("=" * 60)
    print("FarmTrack Database Seeder")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        print("\n1. Seeding users...")
        users = seed_users(db)
        
        print("\n2. Seeding facilities...")
        facilities = seed_facilities(db)
        
        print("\n3. Seeding animal breeds...")
        breeds = seed_animal_breeds(db)
        
        print("\n4. Seeding animals...")
        animals = seed_animals(db, facilities, users)
        
        print("\n5. Seeding events...")
        events = seed_events(db, animals, facilities, users)
        
        print("\n" + "=" * 60)
        print("Database seeding completed successfully!")
        print(f"Total users: {len(users)}")
        print(f"Total facilities: {len(facilities)}")
        print(f"Total breeds: {len(breeds)}")
        print(f"Total animals: {len(animals)}")
        print(f"Total events: {len(events)}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
