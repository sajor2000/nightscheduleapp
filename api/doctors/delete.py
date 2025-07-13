from flask import jsonify
from _shared import create_app, db, Doctor

app = create_app()

def handler(request):
    """Handle individual doctor operations by ID"""
    with app.app_context():
        doctor_id = request.query.get('id')
        
        if not doctor_id:
            return jsonify({'error': 'Doctor ID is required'}), 400
        
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        if request.method == 'DELETE':
            # Deactivate doctor
            doctor.active = False
            try:
                db.session.commit()
                return jsonify({'message': f'{doctor.name} has been deactivated'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'Failed to deactivate doctor'}), 500
        
        else:
            return jsonify({'error': 'Method not allowed'}), 405