import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Shared database instance
db = SQLAlchemy()

def create_app():
    """Create and configure Flask app for serverless functions"""
    app = Flask(__name__)
    
    # Database configuration for Supabase
    database_url = os.getenv('DATABASE_URL', os.getenv('SUPABASE_DB_URL', 'postgresql://localhost/micu_scheduler'))
    if database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
    }
    
    # CORS configuration for Vercel
    CORS(app, 
         origins=[
             'http://localhost:3000',  # Local development
             'https://*.vercel.app',   # Vercel deployments
             'https://nightscheduleapp.vercel.app',  # Production
         ],
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'DELETE', 'PATCH', 'OPTIONS'],
         supports_credentials=True
    )
    
    db.init_app(app)
    
    return app

# Models
class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    initials = db.Column(db.String(4), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'initials': self.initials,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Preference(db.Model):
    __tablename__ = 'preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    month = db.Column(db.String(7), nullable=False)  # YYYY-MM format
    unavailable = db.Column(db.ARRAY(db.String), default=[])
    preferred = db.Column(db.ARRAY(db.String), default=[])
    desired_shifts = db.Column(db.Integer, default=7)
    submitted_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationships
    doctor = db.relationship('Doctor', backref='preferences')
    
    def to_dict(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'doctor_initials': self.doctor.initials if self.doctor else None,
            'month': self.month,
            'unavailable': self.unavailable or [],
            'preferred': self.preferred or [],
            'desired_shifts': self.desired_shifts,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }

class Schedule(db.Model):
    __tablename__ = 'schedule'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    month = db.Column(db.String(7), nullable=False)  # YYYY-MM format
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationships
    doctor = db.relationship('Doctor', backref='schedules')
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'month': self.month,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'doctor_initials': self.doctor.initials if self.doctor else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }