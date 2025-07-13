# Deployment Guide - Vercel + Supabase

## Overview

This application uses **Vercel** for hosting both frontend and backend, with **Supabase** for PostgreSQL database hosting. This provides:

- **Frontend**: React app served by Vercel
- **Backend**: Flask API as Vercel serverless functions  
- **Database**: PostgreSQL hosted on Supabase
- **Cost**: Free tier available for both platforms
- **Performance**: Global CDN and edge functions

## Prerequisites

1. GitHub repository with the code
2. [Vercel account](https://vercel.com)
3. [Supabase account](https://supabase.com)

## Step 1: Supabase Database Setup

### 1.1 Create Supabase Project
1. Go to [Supabase](https://supabase.com)
2. Create new project
3. Choose a region close to your users
4. Note down your database password

### 1.2 Get Database Connection String
1. In Supabase dashboard → Settings → Database
2. Copy the connection string (URI format)
3. It will look like: `postgresql://postgres.xxx:password@db.xxx.supabase.co:5432/postgres`

### 1.3 Initialize Database Schema
1. In Supabase dashboard → SQL Editor
2. Run the schema from `/database/schema.sql`:

```sql
-- Create doctors table
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    initials TEXT UNIQUE NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create preferences table  
CREATE TABLE preferences (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id),
    month VARCHAR(7) NOT NULL,
    unavailable TEXT[] DEFAULT '{}',
    preferred TEXT[] DEFAULT '{}',
    desired_shifts INTEGER DEFAULT 7,
    submitted_at TIMESTAMP DEFAULT NOW()
);

-- Create schedule table
CREATE TABLE schedule (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    month VARCHAR(7) NOT NULL,
    doctor_id INTEGER REFERENCES doctors(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert sample doctors (25 Rush MICU doctors)
INSERT INTO doctors (name, initials) VALUES
('Dr. Sarah Johnson', 'SJ'),
('Dr. Michael Chen', 'MC'),
('Dr. Emily Rodriguez', 'ER'),
-- ... (add all 25 doctors from schema.sql)
```

## Step 2: Vercel Deployment

### 2.1 Import Repository
1. Go to [Vercel dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect it as a React app

### 2.2 Configure Build Settings
Vercel will automatically use the `vercel.json` configuration:
- **Framework**: Create React App (auto-detected)
- **Build Command**: `cd frontend && npm run build`
- **Output Directory**: `frontend/build`
- **Install Command**: `cd frontend && npm install`

### 2.3 Environment Variables
Add these in Vercel dashboard → Settings → Environment Variables:

```bash
# Database (from Supabase)
DATABASE_URL=postgresql://postgres.xxx:password@db.xxx.supabase.co:5432/postgres

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# Python Path for serverless functions
PYTHONPATH=/var/task
```

### 2.4 Deploy
1. Click "Deploy"
2. Vercel will:
   - Install dependencies
   - Build React frontend
   - Deploy serverless functions to `/api/*`
   - Provide your live URL

## Step 3: Verify Deployment

### 3.1 Test Health Check
Visit: `https://your-app.vercel.app/api/health`

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "database": "connected",
  "platform": "vercel"
}
```

### 3.2 Test Frontend
Visit: `https://your-app.vercel.app`
- Should load the React application
- Navigate to all pages (/submit, /admin, /doctors)
- Test basic functionality

## Development Workflow

### Local Development with Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Link Project**:
   ```bash
   vercel link
   ```

3. **Pull Environment Variables**:
   ```bash
   vercel env pull .env.local
   ```

4. **Run Development Server**:
   ```bash
   vercel dev
   ```

This runs:
- React frontend at `http://localhost:3000`
- Serverless functions at `http://localhost:3000/api/*`

### Project Structure for Vercel

```
micu-scheduler/
├── api/                          # Serverless functions
│   ├── _shared.py               # Shared utilities & models
│   ├── health.py                # Health check
│   ├── doctors.py               # Doctor management
│   ├── doctors/
│   │   ├── delete.py           # Delete doctor
│   │   └── activate.py         # Activate doctor
│   ├── submit.py                # Submit preferences
│   ├── preferences.py           # Get preferences
│   ├── generate.py              # Generate schedule
│   ├── schedule.py              # Get schedule
│   ├── export/
│   │   ├── pdf.py              # Export PDF
│   │   └── ics.py              # Export ICS
│   ├── scheduler.py             # Scheduling algorithm
│   └── export_utils.py          # Export utilities
├── frontend/                     # React application
│   ├── src/
│   ├── public/
│   └── package.json
├── vercel.json                   # Vercel configuration
├── requirements.txt              # Python dependencies
└── .env.local                   # Environment variables
```

## API Endpoints

All endpoints are serverless functions at `/api/*`:

- `GET /api/health` - Health check
- `GET /api/doctors` - List doctors
- `POST /api/doctors` - Add doctor
- `DELETE /api/doctors/delete?id=X` - Deactivate doctor
- `POST /api/doctors/activate?id=X` - Activate doctor
- `POST /api/submit` - Submit preferences
- `GET /api/preferences?month=YYYY-MM` - Get preferences
- `POST /api/generate?month=YYYY-MM` - Generate schedule
- `GET /api/schedule?month=YYYY-MM` - Get schedule
- `GET /api/export/pdf?month=YYYY-MM` - Export PDF
- `GET /api/export/ics?month=YYYY-MM&doctor=XX` - Export ICS

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify DATABASE_URL is correct
   - Check Supabase project is active
   - Ensure IP restrictions allow Vercel

2. **Serverless Function Timeouts**
   - Check function logs in Vercel dashboard
   - Optimize database queries
   - Consider upgrading Vercel plan

3. **CORS Issues**
   - Verify domain in CORS settings
   - Check API_BASE_URL configuration

### Monitoring

- **Vercel Analytics**: Monitor performance and usage
- **Supabase Monitoring**: Track database performance
- **Error Tracking**: Check Vercel function logs

## Scaling Considerations

### Free Tier Limits
- **Vercel**: 100GB bandwidth, 6000 minutes compute
- **Supabase**: 500MB database, 2GB bandwidth

### Performance Optimization
- Enable Vercel Edge Functions for better performance
- Use Supabase connection pooling
- Implement caching strategies
- Optimize database queries

## Security

### Best Practices
- Never commit environment variables
- Use Vercel's secure environment management
- Enable Supabase RLS (Row Level Security) if needed
- Use HTTPS only (automatically handled)
- Regular database backups via Supabase

This deployment strategy provides a modern, scalable, and cost-effective solution for the MICU Scheduler application.