"""
Migration: Add breed_id column to animals table
Run with: docker exec traceability_api python -m app.db.migrations.add_breed_to_animals
"""
from app.db.session import SessionLocal, engine
from sqlalchemy import text

def migrate():
    """Add breed_id column to animals table"""
    db = SessionLocal()
    
    try:
        # Check if column exists
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='animals' AND column_name='breed_id'
        """))
        
        if result.fetchone() is None:
            print("Adding breed_id column to animals table...")
            db.execute(text("""
                ALTER TABLE animals 
                ADD COLUMN breed_id INTEGER REFERENCES animal_breeds(id)
            """))
            db.commit()
            print("✓ breed_id column added successfully")
        else:
            print("breed_id column already exists")
            
    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
