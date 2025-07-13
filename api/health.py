from flask import Flask, jsonify
from datetime import datetime
from _shared import create_app, db

def handler(request):
    """Health check endpoint for Vercel"""
    app = create_app()
    
    with app.app_context():
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            response_data = {
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'database': 'connected',
                'platform': 'vercel'
            }
            return jsonify(response_data), 200
        except Exception as e:
            response_data = {
                'status': 'unhealthy',
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }
            return jsonify(response_data), 503