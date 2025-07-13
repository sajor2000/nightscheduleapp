from flask import request, send_file
from _shared import create_app, db, Schedule, Doctor
from export_utils import generate_ics
import io

app = create_app()

def handler(request):
    """Export individual doctor schedule as ICS"""
    with app.app_context():
        if request.method == 'GET':
            month = request.args.get('month')
            doctor_initials = request.args.get('doctor')
            
            if not month or not doctor_initials:
                return {'error': 'Month and doctor parameters are required'}, 400
            
            try:
                # Find doctor by initials
                doctor = Doctor.query.filter_by(initials=doctor_initials).first()
                if not doctor:
                    return {'error': 'Doctor not found'}, 404
                
                # Get schedules for this doctor in this month
                schedules = Schedule.query.filter_by(
                    month=month, 
                    doctor_id=doctor.id
                ).all()
                
                # Generate ICS
                ics_content = generate_ics(month, doctor.name, schedules)
                
                # Return as file
                output = io.BytesIO(ics_content.encode('utf-8'))
                output.seek(0)
                
                filename = f"micu_schedule_{doctor_initials}_{month}.ics"
                return send_file(output, 
                               mimetype='text/calendar', 
                               as_attachment=True,
                               download_name=filename)
                
            except Exception as e:
                return {'error': f'Failed to generate ICS: {str(e)}'}, 500
        
        else:
            return {'error': 'Method not allowed'}, 405