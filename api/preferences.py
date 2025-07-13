from flask import request, jsonify
from _shared import create_app, db, Preference

app = create_app()

def handler(request):
    """Get preferences for a specific month"""
    with app.app_context():
        if request.method == 'GET':
            month = request.args.get('month')
            if not month:
                return jsonify({'error': 'Month parameter is required'}), 400
            
            preferences = Preference.query.filter_by(month=month).all()
            return jsonify([p.to_dict() for p in preferences])
        
        else:
            return jsonify({'error': 'Method not allowed'}), 405