from flask import request, jsonify
from datetime import datetime
from _shared import create_app, db, Schedule, Preference
from scheduler import generate_schedule

app = create_app()

def handler(request):
    """Generate schedule for a specific month"""
    with app.app_context():
        if request.method == 'POST':
            month = request.args.get('month')
            if not month:
                return jsonify({'error': 'Month parameter is required'}), 400
            
            # Get preferences for the month
            preferences = Preference.query.filter_by(month=month).all()
            if not preferences:
                return jsonify({'error': 'No preferences found for this month'}), 400
            
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
                
                return jsonify({
                    'message': 'Schedule generated successfully',
                    'assignments': len(new_schedule),
                    'schedule': new_schedule
                })
                
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Failed to generate schedule: {str(e)}'}), 500
        
        else:
            return jsonify({'error': 'Method not allowed'}), 405