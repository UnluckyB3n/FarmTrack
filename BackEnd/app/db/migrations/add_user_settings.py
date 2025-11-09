"""
Add user profile and settings columns

This migration adds columns for user profile, account, and notification settings.
"""

from sqlalchemy import Column, String, Boolean, Text
from app.db.session import engine
from app.db.models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upgrade():
    """Add new columns to users table"""
    logger.info("Starting migration: Adding profile and settings columns to users table")
    
    try:
        # Get connection
        with engine.connect() as conn:
            # Check if columns already exist
            result = conn.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name='users'"
            )
            existing_columns = [row[0] for row in result]
            
            # Add email column if it doesn't exist
            if 'email' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN email VARCHAR UNIQUE")
                conn.commit()
                logger.info("Added column: email")
            
            # Add full_name column if it doesn't exist
            if 'full_name' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN full_name VARCHAR")
                conn.commit()
                logger.info("Added column: full_name")
            
            # Add bio column if it doesn't exist
            if 'bio' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN bio TEXT")
                conn.commit()
                logger.info("Added column: bio")
            
            # Add date_of_birth column if it doesn't exist
            if 'date_of_birth' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN date_of_birth VARCHAR")
                conn.commit()
                logger.info("Added column: date_of_birth")
            
            # Add language column if it doesn't exist
            if 'language' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN language VARCHAR DEFAULT 'en'")
                conn.commit()
                logger.info("Added column: language")
            
            # Add marketing_emails column if it doesn't exist
            if 'marketing_emails' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN marketing_emails BOOLEAN DEFAULT TRUE")
                conn.commit()
                logger.info("Added column: marketing_emails")
            
            # Add social_emails column if it doesn't exist
            if 'social_emails' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN social_emails BOOLEAN DEFAULT TRUE")
                conn.commit()
                logger.info("Added column: social_emails")
            
            # Add security_emails column if it doesn't exist
            if 'security_emails' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN security_emails BOOLEAN DEFAULT TRUE")
                conn.commit()
                logger.info("Added column: security_emails")
            
            # Add communication_emails column if it doesn't exist
            if 'communication_emails' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN communication_emails BOOLEAN DEFAULT FALSE")
                conn.commit()
                logger.info("Added column: communication_emails")
            
            # Add mobile_notifications column if it doesn't exist
            if 'mobile_notifications' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN mobile_notifications BOOLEAN DEFAULT FALSE")
                conn.commit()
                logger.info("Added column: mobile_notifications")
        
        logger.info("Migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise


if __name__ == "__main__":
    upgrade()
