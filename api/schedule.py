from flask import request, jsonify
from _shared import create_app, db, Schedule

app = create_app()

def handler(request):
    """Get schedule for a specific month"""
    with app.app_context():
        if request.method == 'GET':
            month = request.args.get('month')
            if not month:
                return jsonify({'error': 'Month parameter is required'}), 400
            
            schedule = Schedule.query.filter_by(month=month).order_by(Schedule.date).all()
            return jsonify([s.to_dict() for s in schedule])
        
        else:
            return jsonify({'error': 'Method not allowed'}), 405