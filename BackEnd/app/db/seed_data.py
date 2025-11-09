"""
Database seeder script to populate FarmTrack with realistic data
Run with: python -m app.db.seed_data
"""
from datetime import datetime, timedelta
import random
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
    """Create sample animal breeds"""
    breeds_data = [
        {"country": "United States", "iso3": "USA", "specie": "Cattle", "breed_name": "Angus", "language": "English", 
         "description": "Black beef cattle breed known for marbling quality"},
        {"country": "United States", "iso3": "USA", "specie": "Cattle", "breed_name": "Hereford", "language": "English",
         "description": "Red cattle with white face, hardy and efficient"},
        {"country": "Switzerland", "iso3": "CHE", "specie": "Cattle", "breed_name": "Holstein", "language": "English",
         "description": "Black and white dairy cattle, high milk production"},
        {"country": "United Kingdom", "iso3": "GBR", "specie": "Sheep", "breed_name": "Suffolk", "language": "English",
         "description": "Large meat sheep with black face and legs"},
        {"country": "Spain", "iso3": "ESP", "specie": "Sheep", "breed_name": "Merino", "language": "English",
         "description": "Famous for fine wool production"},
        {"country": "United Kingdom", "iso3": "GBR", "specie": "Pig", "breed_name": "Yorkshire", "language": "English",
         "description": "Large white pig, excellent for bacon"},
        {"country": "United States", "iso3": "USA", "specie": "Pig", "breed_name": "Duroc", "language": "English",
         "description": "Red pig known for fast growth and meat quality"},
        {"country": "France", "iso3": "FRA", "specie": "Goat", "breed_name": "Alpine", "language": "English",
         "description": "Dairy goat breed with high milk production"},
    ]
    
    breeds = []
    for data in breeds_data:
        existing = db.query(AnimalBreed).filter(
            AnimalBreed.breed_name == data["breed_name"],
            AnimalBreed.specie == data["specie"]
        ).first()
        if not existing:
            breed = AnimalBreed(**data)
            db.add(breed)
            breeds.append(breed)
            print(f"Created breed: {data['breed_name']}")
        else:
            breeds.append(existing)
    
    db.commit()
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
