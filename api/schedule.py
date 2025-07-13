import json
import urllib.parse

def handler(request):
    """Get schedule for a specific month"""
    try:
        from _shared import create_app, db, Schedule
        
        app = create_app()
        
        with app.app_context():
            if request.method == 'GET':
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
                
                schedule = Schedule.query.filter_by(month=month).order_by(Schedule.date).all()
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps([s.to_dict() for s in schedule])
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