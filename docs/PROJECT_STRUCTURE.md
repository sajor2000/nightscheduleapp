# Project Structure

```
micu-scheduler/
├── backend/                    # Flask API backend
│   ├── app.py                 # Main Flask application
│   ├── models.py              # SQLAlchemy database models
│   ├── scheduler.py           # Scheduling algorithm implementation
│   ├── export_utils.py        # PDF and ICS export utilities
│   ├── init_db.py            # Database initialization script
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React frontend application
│   ├── public/                # Static files
│   │   ├── index.html        # HTML template
│   │   └── favicon.svg       # Rush-branded favicon
│   ├── src/
│   │   ├── components/       # Reusable React components
│   │   ├── pages/           # Page components
│   │   │   ├── Submit.js    # Doctor availability submission
│   │   │   ├── Admin.js     # Admin dashboard
│   │   │   └── Doctors.js   # Doctor management
│   │   ├── styles/          # Global styles
│   │   │   ├── globals.css  # CSS variables and base styles
│   │   │   └── print.css    # Print-specific styles
│   │   ├── App.js          # Main app component
│   │   ├── App.css         # App-specific styles
│   │   └── index.js        # Entry point
│   └── package.json        # Node dependencies
│
├── database/                  # Database files
│   └── schema.sql           # PostgreSQL schema definition
│
├── docs/                     # Documentation
│   └── PROJECT_STRUCTURE.md # This file
│
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
├── .replit                 # Replit configuration
├── replit.nix             # Replit Nix packages
├── run.sh                 # Startup script for deployment
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Contribution guidelines
└── README.md             # Project documentation
```

## Key Directories

### Backend (`/backend`)
Contains the Flask API server that handles:
- Doctor management
- Preference submission
- Schedule generation
- Export functionality

### Frontend (`/frontend`)
React application with:
- Material Design-inspired UI
- Rush University branding
- Responsive design
- Print optimization

### Database (`/database`)
PostgreSQL schema and migrations for:
- Doctors table
- Preferences table
- Schedule table