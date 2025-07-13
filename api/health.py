from flask import Flask, jsonify
from datetime import datetime
import json

def handler(request):
    """Health check endpoint for Vercel"""
    try:
        # Import here to avoid issues with serverless cold starts
        from _shared import create_app, db
        
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
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(response_data)
                }
            except Exception as db_error:
                response_data = {
                    'status': 'unhealthy',
                    'timestamp': datetime.utcnow().isoformat(),
                    'error': str(db_error),
                    'database': 'disconnected'
                }
                return {
                    'statusCode': 503,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(response_data)
                }
    except Exception as e:
        # Fallback error response
        response_data = {
            'status': 'error',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e),
            'platform': 'vercel'
        }
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response_data)
        }