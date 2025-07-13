from flask import request, jsonify
from _shared import create_app, db, Preference, Doctor

app = create_app()

def handler(request):
    """Submit doctor preferences"""
    with app.app_context():
        # Ensure tables exist
        db.create_all()
        
        if request.method == 'POST':
            data = request.get_json()
            
            required_fields = ['doctor_id', 'month', 'desired_shifts']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Validate doctor exists
            doctor = Doctor.query.get(data['doctor_id'])
            if not doctor:
                return jsonify({'error': 'Doctor not found'}), 404
            
            # Check if preferences already exist for this month
            existing = Preference.query.filter_by(
                doctor_id=data['doctor_id'],
                month=data['month']
            ).first()
            
            if existing:
                # Update existing preferences
                existing.unavailable = data.get('unavailable', [])
                existing.preferred = data.get('preferred', [])
                existing.desired_shifts = data['desired_shifts']
                preference = existing
            else:
                # Create new preferences
                preference = Preference(
                    doctor_id=data['doctor_id'],
                    month=data['month'],
                    unavailable=data.get('unavailable', []),
                    preferred=data.get('preferred', []),
                    desired_shifts=data['desired_shifts']
                )
                db.session.add(preference)
            
            try:
                db.session.commit()
                return jsonify({
                    'message': 'Preferences submitted successfully',
                    'preference': preference.to_dict()
                })
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'Failed to submit preferences'}), 500
        
        else:
            return jsonify({'error': 'Method not allowed'}), 405