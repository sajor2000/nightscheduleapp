import json
import urllib.parse
from datetime import datetime

def handler(request):
    """Generate schedule for a specific month"""
    try:
        from _shared import create_app, db, Schedule, Preference
        from scheduler import generate_schedule
        
        app = create_app()
        
        with app.app_context():
            if request.method == 'POST':
                # Get month parameter from query
                month = None
                if hasattr(request, 'args'):
                    month = request.args.get('month')
                elif hasattr(request, 'query'):
                    month = request.query.get('month')
                elif hasattr(request, 'url'):
                    # Parse URL for query parameters
                    parsed = urllib.parse.urlparse(request.url)
                    query_params = urllib.parse.parse_qs(parsed.query)
                    month = query_params.get('month', [None])[0]
                
                if not month:
                    return {
                        'statusCode': 400,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'Month parameter is required'})
                    }
                
                # Get preferences for the month
                preferences = Preference.query.filter_by(month=month).all()
                if not preferences:
                    return {
                        'statusCode': 400,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'No preferences found for this month'})
                    }
                
                # Get existing schedule
                existing_schedule = {}
                existing_assignments = Schedule.query.filter_by(month=month).all()
                for assignment in existing_assignments:
                    existing_schedule[assignment.date.strftime('%Y-%m-%d')] = assignment.doctor_id
                
                # Convert preferences to the format expected by scheduler
                preferences_data = [p.to_dict() for p in preferences]
                
                try:
                    # Generate new schedule
                    new_schedule = generate_schedule(month, preferences_data, existing_schedule)
                    
                    # Clear existing schedule for the month
                    Schedule.query.filter_by(month=month).delete()
                    
                    # Save new schedule
                    for date_str, doctor_id in new_schedule.items():
                        if doctor_id:  # Only save assigned dates
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                            schedule_entry = Schedule(
                                date=date_obj,
                                month=month,
                                doctor_id=doctor_id
                            )
                            db.session.add(schedule_entry)
                    
                    db.session.commit()
                    
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            'message': 'Schedule generated successfully',
                            'assignments': len(new_schedule),
                            'schedule': new_schedule
                        })
                    }
                    
                except Exception as e:
                    db.session.rollback()
                    return {
                        'statusCode': 500,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': f'Failed to generate schedule: {str(e)}'})
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