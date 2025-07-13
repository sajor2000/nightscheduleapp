import json
import urllib.parse

def handler(request):
    """Handle doctor-related operations"""
    try:
        from _shared import create_app, db, Doctor
        
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
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps([d.to_dict() for d in doctors])
                }
            
            elif request.method == 'POST':
                # Add new doctor
                try:
                    body = json.loads(request.body) if hasattr(request, 'body') else request.get_json()
                except:
                    return {
                        'statusCode': 400,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'Invalid JSON in request body'})
                    }
                
                if not body.get('name') or not body.get('initials'):
                    return {
                        'statusCode': 400,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'Name and initials are required'})
                    }
                
                # Check if initials already exist
                existing = Doctor.query.filter_by(initials=body['initials']).first()
                if existing:
                    return {
                        'statusCode': 400,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'Doctor with these initials already exists'})
                    }
                
                doctor = Doctor(
                    name=body['name'],
                    initials=body['initials'].upper()
                )
                
                try:
                    db.session.add(doctor)
                    db.session.commit()
                    return {
                        'statusCode': 201,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps(doctor.to_dict())
                    }
                except Exception as e:
                    db.session.rollback()
                    return {
                        'statusCode': 500,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'Failed to add doctor'})
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