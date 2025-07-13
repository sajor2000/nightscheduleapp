from flask import request, jsonify
from _shared import create_app, db, Doctor

def handler(request):
    """Handle doctor-related operations"""
    app = create_app()
    
    with app.app_context():
        # Ensure tables exist
        db.create_all()
        
        if request.method == 'GET':
            # Get all doctors
            active_only = request.args.get('active', 'true').lower() == 'true'
            query = Doctor.query
            if active_only:
                query = query.filter_by(active=True)
            doctors = query.order_by(Doctor.name).all()
            return jsonify([d.to_dict() for d in doctors])
        
        elif request.method == 'POST':
            # Add new doctor
            data = request.get_json()
            if not data.get('name') or not data.get('initials'):
                return jsonify({'error': 'Name and initials are required'}), 400
            
            # Check if initials already exist
            existing = Doctor.query.filter_by(initials=data['initials']).first()
            if existing:
                return jsonify({'error': 'Doctor with these initials already exists'}), 400
            
            doctor = Doctor(
                name=data['name'],
                initials=data['initials'].upper()
            )
            
            try:
                db.session.add(doctor)
                db.session.commit()
                return jsonify(doctor.to_dict()), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'Failed to add doctor'}), 500
        
        else:
            return jsonify({'error': 'Method not allowed'}), 405