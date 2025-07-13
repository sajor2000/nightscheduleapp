#!/usr/bin/env python3
"""
Initialize the database with the schema and preloaded doctors.
Run this script after setting up your database connection.
"""

from app import app, db
from models import Doctor

# List of doctors to preload
INITIAL_DOCTORS = [
    {"initials": "AK", "name": "Akshay Kohli"},
    {"initials": "AG", "name": "Amie Gamino"},
    {"initials": "AT", "name": "Abhaya Trivedi"},
    {"initials": "BM", "name": "Babak Mokhlesi"},
    {"initials": "BS", "name": "Brian Stein"},
    {"initials": "DG", "name": "David Gurka"},
    {"initials": "EC", "name": "Elaine Chen"},
    {"initials": "EP", "name": "Ed Pickering"},
    {"initials": "JCR", "name": "JC Rojas"},
    {"initials": "JEK", "name": "Jessica Kuppy"},
    {"initials": "JG", "name": "Jared Greenberg"},
    {"initials": "JK", "name": "James Katsis"},
    {"initials": "JN", "name": "Julie Neborak"},
    {"initials": "JR", "name": "James Rowley"},
    {"initials": "KB", "name": "Kevin Buell"},
    {"initials": "KJ", "name": "Kari Jackson"},
    {"initials": "KS", "name": "Kalli Sarigiannis"},
    {"initials": "MS", "name": "Meghan Snuckel"},
    {"initials": "MT", "name": "Mark Tancredi"},
    {"initials": "MV", "name": "Mona Vashi"},
    {"initials": "MY", "name": "Mark Yoder"},
    {"initials": "PN", "name": "Prema Nanavaty"},
    {"initials": "SF", "name": "Sam Fox"},
    {"initials": "SP", "name": "Shruti Patel"},
    {"initials": "WL", "name": "Waj Lodhi"}
]

def init_database():
    """Initialize the database with tables and initial data."""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if doctors already exist
        existing_count = Doctor.query.count()
        if existing_count > 0:
            print(f"ℹ️  Database already contains {existing_count} doctors, skipping initialization")
            return
        
        # Add initial doctors
        for doc_data in INITIAL_DOCTORS:
            doctor = Doctor(
                name=doc_data["name"],
                initials=doc_data["initials"],
                active=True
            )
            db.session.add(doctor)
        
        db.session.commit()
        print(f"✅ Added {len(INITIAL_DOCTORS)} doctors to the database")
        
        # Verify
        final_count = Doctor.query.count()
        print(f"✅ Database now contains {final_count} doctors")

if __name__ == "__main__":
    init_database()