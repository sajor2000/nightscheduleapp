import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
from models import db, Doctor, Preference, Schedule
from scheduler import generate_schedule, validate_schedule
from export_utils import generate_ics, generate_pdf
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/micu_scheduler')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()

# Doctor routes
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    active_only = request.args.get('active', 'true').lower() == 'true'
    query = Doctor.query
    if active_only:
        query = query.filter_by(active=True)
    doctors = query.order_by(Doctor.name).all()
    return jsonify([d.to_dict() for d in doctors])

@app.route('/api/doctors', methods=['POST'])
def add_doctor():
    data = request.json
    if not data.get('name') or not data.get('initials'):
        return jsonify({'error': 'Name and initials are required'}), 400
    
    # Check if initials already exist
    existing = Doctor.query.filter_by(initials=data['initials']).first()
    if existing:
        return jsonify({'error': 'Doctor with these initials already exists'}), 400
    
    doctor = Doctor(
        name=data['name'],
        initials=data['initials']
    )
    db.session.add(doctor)
    db.session.commit()
    
    return jsonify(doctor.to_dict()), 201

@app.route('/api/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.active = False
    db.session.commit()
    return jsonify({'message': 'Doctor deactivated successfully'})

@app.route('/api/doctors/<int:doctor_id>/activate', methods=['POST'])
def activate_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.active = True
    db.session.commit()
    return jsonify(doctor.to_dict())

@app.route('/api/doctors/<int:doctor_id>/toggle', methods=['PATCH'])
def toggle_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.active = not doctor.active
    db.session.commit()
    return jsonify(doctor.to_dict())

# Preference routes
@app.route('/api/preferences', methods=['GET'])
def get_preferences():
    month = request.args.get('month')
    if not month:
        return jsonify({'error': 'Month parameter is required'}), 400
    
    preferences = Preference.query.filter_by(month=month).all()
    return jsonify([p.to_dict() for p in preferences])

@app.route('/api/submit', methods=['POST'])
def submit_preferences():
    data = request.json
    required = ['doctor_id', 'month', 'unavailable', 'preferred', 'desired_shifts']
    
    for field in required:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if preferences already exist
    existing = Preference.query.filter_by(
        doctor_id=data['doctor_id'],
        month=data['month']
    ).first()
    
    if existing:
        # Update existing preferences
        existing.unavailable = data['unavailable']
        existing.preferred = data['preferred']
        existing.desired_shifts = data['desired_shifts']
    else:
        # Create new preferences
        pref = Preference(
            doctor_id=data['doctor_id'],
            month=data['month'],
            unavailable=data['unavailable'],
            preferred=data['preferred'],
            desired_shifts=data['desired_shifts']
        )
        db.session.add(pref)
    
    db.session.commit()
    return jsonify({'message': 'Preferences submitted successfully'}), 201

# Schedule routes
@app.route('/api/generate', methods=['POST'])
def generate():
    month = request.args.get('month')
    if not month:
        return jsonify({'error': 'Month parameter is required'}), 400
    
    # Get all preferences for the month
    preferences = Preference.query.filter_by(month=month).all()
    if not preferences:
        return jsonify({'error': 'No preferences found for this month'}), 400
    
    prefs_data = [p.to_dict() for p in preferences]
    
    # Get existing schedule if any
    existing_schedule = {}
    schedules = Schedule.query.filter_by(month=month).all()
    for s in schedules:
        existing_schedule[s.date.isoformat()] = s.doctor_id
    
    # Generate new schedule
    new_schedule = generate_schedule(month, prefs_data, existing_schedule)
    
    # Validate schedule
    is_valid, errors = validate_schedule(new_schedule, prefs_data)
    if not is_valid:
        return jsonify({'errors': errors}), 400
    
    # Save schedule to database
    # First, delete old unmodified entries
    Schedule.query.filter_by(month=month).delete()
    
    # Add new schedule entries
    for date_str, doctor_id in new_schedule.items():
        schedule_entry = Schedule(
            doctor_id=doctor_id,
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            month=month
        )
        db.session.add(schedule_entry)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Schedule generated successfully',
        'schedule': new_schedule
    })

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    month = request.args.get('month')
    if not month:
        return jsonify({'error': 'Month parameter is required'}), 400
    
    schedules = Schedule.query.filter_by(month=month).all()
    return jsonify([s.to_dict() for s in schedules])

@app.route('/api/schedule/edit', methods=['POST'])
def edit_schedule():
    data = request.json
    date_str = data.get('date')
    doctor_id = data.get('doctor_id')
    
    if not date_str:
        return jsonify({'error': 'Date is required'}), 400
    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    month = date_str[:7]
    
    # Find existing schedule entry
    schedule = Schedule.query.filter_by(date=date_obj).first()
    
    if doctor_id:
        # Update or create
        if schedule:
            schedule.doctor_id = doctor_id
            schedule.modified_at = datetime.utcnow()
        else:
            schedule = Schedule(
                doctor_id=doctor_id,
                date=date_obj,
                month=month
            )
            db.session.add(schedule)
    else:
        # Delete assignment
        if schedule:
            db.session.delete(schedule)
    
    db.session.commit()
    return jsonify({'message': 'Schedule updated successfully'})

# Export routes
@app.route('/api/export/ics', methods=['GET'])
def export_ics():
    month = request.args.get('month')
    doctor_initials = request.args.get('doctor')
    
    if not month or not doctor_initials:
        return jsonify({'error': 'Month and doctor parameters are required'}), 400
    
    # Get doctor
    doctor = Doctor.query.filter_by(initials=doctor_initials).first()
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    # Get schedule for doctor
    schedules = Schedule.query.filter_by(month=month, doctor_id=doctor.id).all()
    
    # Generate ICS file
    ics_content = generate_ics(doctor, schedules, month)
    
    # Return as file
    output = io.BytesIO()
    output.write(ics_content.encode('utf-8'))
    output.seek(0)
    
    filename = f"micu_schedule_{doctor.initials}_{month}.ics"
    return send_file(output, mimetype='text/calendar', as_attachment=True, 
                     attachment_filename=filename)

@app.route('/api/export/pdf', methods=['GET'])
def export_pdf():
    month = request.args.get('month')
    if not month:
        return jsonify({'error': 'Month parameter is required'}), 400
    
    # Get all schedules for the month
    schedules = Schedule.query.filter_by(month=month).all()
    
    # Get all preferences for highlighting
    preferences = Preference.query.filter_by(month=month).all()
    
    # Generate PDF
    pdf_bytes = generate_pdf(month, schedules, preferences)
    
    # Return as file
    output = io.BytesIO(pdf_bytes)
    output.seek(0)
    
    filename = f"micu_schedule_{month}.pdf"
    return send_file(output, mimetype='application/pdf', as_attachment=True,
                     attachment_filename=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)