# Project Structure - Vercel + Supabase

```
micu-scheduler/
├── README.md                    # Main project documentation
├── LICENSE                      # MIT license
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment variables template
├── vercel.json                 # Vercel deployment configuration
├── requirements.txt            # Python dependencies for serverless functions
├── 
├── api/                        # Vercel Serverless Functions (Backend)
│   ├── _shared.py             # Shared utilities & models
│   ├── health.py              # Health check endpoint
│   ├── doctors.py             # Doctor management
│   ├── doctors/
│   │   ├── delete.py          # Deactivate doctor
│   │   └── activate.py        # Activate doctor
│   ├── submit.py              # Submit preferences
│   ├── preferences.py         # Get preferences
│   ├── generate.py            # Generate schedule
│   ├── schedule.py            # Get schedule
│   ├── export/
│   │   ├── pdf.py            # Export PDF
│   │   └── ics.py            # Export ICS
│   ├── scheduler.py           # Scheduling algorithm
│   └── export_utils.py        # PDF/ICS generation utilities
├── 
├── frontend/                   # React Application
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.svg
│   ├── src/
│   │   ├── index.js          # App entry point
│   │   ├── App.js            # Main app component
│   │   ├── config/
│   │   │   └── api.js        # API configuration
│   │   ├── pages/
│   │   │   ├── Submit.js     # Doctor preference submission
│   │   │   ├── Admin.js      # Schedule management
│   │   │   └── Doctors.js    # Doctor management
│   │   └── styles/
│   │       ├── globals.css   # Global Rush-branded styles
│   │       └── print.css     # Print-specific styles
│   ├── .env.development       # Development environment
│   ├── .env.production        # Production environment
│   ├── .env.example          # Environment template
│   ├── package.json
│   └── package-lock.json
├── 
├── database/                   # Supabase Database Scripts
│   ├── schema.sql             # Original PostgreSQL schema
│   ├── supabase_schema.sql    # Production Supabase schema
│   ├── supabase_seed.sql      # Test data for development
│   ├── supabase_verify.sql    # Verification queries
│   └── supabase_cleanup.sql   # Reset script
├── 
└── docs/                       # Documentation
    ├── DEPLOYMENT.md          # Vercel + Supabase deployment guide
    ├── SUPABASE_SETUP.md      # Database setup instructions
    └── PROJECT_STRUCTURE.md   # This file
```

## Architecture Overview

### Frontend (React)
- **Hosting**: Vercel CDN
- **Framework**: Create React App
- **Styling**: Rush University branding with CSS variables
- **API Integration**: Axios with centralized endpoint configuration

### Backend (Serverless Functions)
- **Hosting**: Vercel serverless functions at `/api/*`
- **Runtime**: Python 3.9
- **Framework**: Flask with SQLAlchemy
- **Database**: PostgreSQL on Supabase

### Database (Supabase)
- **Type**: PostgreSQL 14+
- **Tables**: doctors, preferences, schedule
- **Features**: Arrays, constraints, indexes, triggers
- **Location**: Global edge network

## Deployment Flow

1. **Code Push** → GitHub repository
2. **Auto Deploy** → Vercel builds and deploys
3. **Frontend** → Served from Vercel CDN
4. **API Calls** → Routed to serverless functions
5. **Database** → Connected to Supabase PostgreSQL

## Environment Configuration

- **Development**: Local with `vercel dev`
- **Production**: Vercel + Supabase cloud
- **Environment Variables**: Managed in Vercel dashboard

## Key Features

### Serverless Architecture
- **Scalability**: Auto-scaling based on demand
- **Cost**: Pay-per-execution model
- **Performance**: Global edge functions

### Modern Stack
- **Frontend**: React 18 with hooks
- **Backend**: Python Flask serverless functions
- **Database**: PostgreSQL with modern features
- **Deployment**: Git-based continuous deployment