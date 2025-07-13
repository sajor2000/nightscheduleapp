import json
import urllib.parse

def handler(request):
    """Activate a doctor"""
    try:
        from _shared import create_app, db, Doctor
        
        app = create_app()
        
        with app.app_context():
            # Get doctor ID from query parameters
            doctor_id = None
            if hasattr(request, 'args'):
                doctor_id = request.args.get('id')
            elif hasattr(request, 'query'):
                doctor_id = request.query.get('id')
            elif hasattr(request, 'url'):
                # Parse URL for query parameters
                parsed = urllib.parse.urlparse(request.url)
                query_params = urllib.parse.parse_qs(parsed.query)
                doctor_id = query_params.get('id', [None])[0]
            
            if not doctor_id:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Doctor ID is required'})
                }
            
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Doctor not found'})
                }
            
            if request.method == 'POST':
                # Activate doctor
                doctor.active = True
                try:
                    db.session.commit()
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'message': f'{doctor.name} has been activated'})
                    }
                except Exception as e:
                    db.session.rollback()
                    return {
                        'statusCode': 500,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'Failed to activate doctor'})
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