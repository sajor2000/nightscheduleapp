from flask import jsonify
from datetime import datetime
from _shared import create_app, db

app = create_app()

def handler(request):
    """Health check endpoint for Vercel"""
    with app.app_context():
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'database': 'connected',
                'platform': 'vercel'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }), 503