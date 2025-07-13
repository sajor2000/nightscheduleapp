# Deployment Guide

## Replit Deployment

1. **Import to Replit**
   - Go to [Replit](https://replit.com)
   - Click "Create Repl"
   - Import from GitHub: `https://github.com/sajor2000/nightscheduleapp`

2. **Environment Setup**
   - The `.replit` and `replit.nix` files are already configured
   - Add PostgreSQL database from Replit's database panel
   - Set `DATABASE_URL` in Replit secrets

3. **Run the Application**
   - Click "Run" button
   - The `run.sh` script will:
     - Install dependencies
     - Initialize database
     - Build React frontend
     - Start Flask server

## Manual Deployment

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
npm run build
```

### Database Setup
```bash
# Create PostgreSQL database
createdb micu_scheduler

# Run schema
psql -d micu_scheduler -f database/schema.sql

# Or use init script
python backend/init_db.py
```

### Environment Variables
```bash
export DATABASE_URL=postgresql://user:password@localhost/micu_scheduler
export FLASK_ENV=production
```

### Production Server
```bash
cd backend
gunicorn app:app --bind 0.0.0.0:5000
```

## Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm

# Copy application
WORKDIR /app
COPY . .

# Install dependencies
RUN cd backend && pip install -r requirements.txt
RUN cd frontend && npm install && npm run build

# Run application
CMD ["bash", "run.sh"]
```

## Security Considerations

1. **Environment Variables**
   - Never commit `.env` files
   - Use secure secrets management
   - Rotate database credentials regularly

2. **HTTPS**
   - Always use HTTPS in production
   - Configure SSL certificates
   - Enable HSTS headers

3. **Database**
   - Use connection pooling
   - Enable SSL for database connections
   - Regular backups

4. **Authentication**
   - Consider adding authentication for production
   - Implement role-based access control
   - Use secure session management