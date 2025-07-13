import json

def handler(request):
    """Submit doctor preferences"""
    try:
        from _shared import create_app, db, Preference, Doctor
        
        app = create_app()
        
        with app.app_context():
            # Ensure tables exist
            db.create_all()
            
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) if hasattr(request, 'body') else request.get_json()
                except:
                    return {
                        'statusCode': 400,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'Invalid JSON in request body'})
                    }
                
                required_fields = ['doctor_id', 'month', 'desired_shifts']
                for field in required_fields:
                    if field not in data:
                        return {
                            'statusCode': 400,
                            'headers': {'Content-Type': 'application/json'},
                            'body': json.dumps({'error': f'{field} is required'})
                        }
                
                # Validate doctor exists
                doctor = Doctor.query.get(data['doctor_id'])
                if not doctor:
                    return {
                        'statusCode': 404,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'Doctor not found'})
                    }
                
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
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            'message': 'Preferences submitted successfully',
                            'preference': preference.to_dict()
                        })
                    }
                except Exception as e:
                    db.session.rollback()
                    return {
                        'statusCode': 500,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'Failed to submit preferences'})
                    }
            
            else:
                return {
                    'statusCode': 405,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Method not allowed'})
                }
                
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Server error: {str(e)}'})
        }