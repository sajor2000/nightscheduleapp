import json
import urllib.parse

def handler(request):
    """Get preferences for a specific month"""
    try:
        from _shared import create_app, db, Preference
        
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
                
                preferences = Preference.query.filter_by(month=month).all()
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps([p.to_dict() for p in preferences])
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