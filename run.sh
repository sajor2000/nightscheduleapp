#!/bin/bash

# Install Python dependencies
echo "Installing Python dependencies..."
cd backend
pip install -r requirements.txt

# Initialize database if needed
echo "Initializing database..."
python init_db.py

# Install Node dependencies and build frontend
echo "Installing Node dependencies..."
cd ../frontend
npm install

echo "Building React app..."
npm run build

# Serve the app
echo "Starting the application..."
cd ../backend

# Serve React build from Flask
export FLASK_ENV=production
python -c "
import os
from flask import send_from_directory
from app import app

# Serve React build
react_build_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != '' and os.path.exists(os.path.join(react_build_path, path)):
        return send_from_directory(react_build_path, path)
    else:
        return send_from_directory(react_build_path, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"