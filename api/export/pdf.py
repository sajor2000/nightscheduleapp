from flask import request, send_file
from _shared import create_app, db, Schedule, Preference
from export_utils import generate_pdf
import io

app = create_app()

def handler(request):
    """Export schedule as PDF"""
    with app.app_context():
        if request.method == 'GET':
            month = request.args.get('month')
            if not month:
                return {'error': 'Month parameter is required'}, 400
            
            try:
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
                return send_file(output, 
                               mimetype='application/pdf', 
                               as_attachment=True,
                               download_name=filename)
                
            except Exception as e:
                return {'error': f'Failed to generate PDF: {str(e)}'}, 500
        
        else:
            return {'error': 'Method not allowed'}, 405