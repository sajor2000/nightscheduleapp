from flask import request, jsonify
from _shared import create_app, db, Doctor

app = create_app()

def handler(request):
    """Activate a doctor"""
    with app.app_context():
        doctor_id = request.query.get('id')
        
        if not doctor_id:
            return jsonify({'error': 'Doctor ID is required'}), 400
        
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        if request.method == 'POST':
            # Activate doctor
            doctor.active = True
            try:
                db.session.commit()
                return jsonify({'message': f'{doctor.name} has been activated'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'Failed to activate doctor'}), 500
        
        else:
            return jsonify({'error': 'Method not allowed'}), 405