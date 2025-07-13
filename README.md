# 🏥 MICU Night Shift Scheduler

A professional web application for scheduling night shifts for physicians at Rush University Medical Center's Medical Intensive Care Unit (MICU).

![Rush University Medical Center](https://img.shields.io/badge/Rush_University-Medical_Center-00573F?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+CiAgPHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iNCIgZmlsbD0iIzAwNTczRiIvPgogIDxwYXRoIGQ9Ik0xNiA0IEwxNiAyOCBNNCAxNiBMMjggMTYiIHN0cm9rZT0iI0NGQjUzQiIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPC9zdmc+)
![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react)
![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=for-the-badge&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-336791?style=for-the-badge&logo=postgresql)

## Features

- **Doctor Availability Submission**: Doctors can submit their monthly availability preferences
- **Automated Scheduling**: Generates optimized schedules based on preferences and constraints
- **Manual Schedule Editing**: Administrators can manually adjust assignments
- **Export Functionality**: 
  - PDF calendar for the entire month
  - ICS calendar files for individual doctors
- **Doctor Management**: Add, deactivate, and reactivate doctors

## Tech Stack

- **Frontend**: React with FullCalendar
- **Backend**: Flask with SQLAlchemy
- **Database**: PostgreSQL
- **Export**: ReportLab (PDF), custom ICS generation

## Setup Instructions

### Local Development

1. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database Setup**:
   - Create a PostgreSQL database
   - Set the `DATABASE_URL` environment variable
   - Run the schema script: `psql -d your_database -f database/schema.sql`

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   ```

4. **Run the Application**:
   - Backend: `cd backend && python app.py`
   - Frontend: `cd frontend && npm start`

### Deployment

The application uses **Vercel + Supabase** for a modern, serverless deployment:
- **Frontend & Backend**: Deployed on [Vercel](https://vercel.com)
- **Database**: Hosted on [Supabase](https://supabase.com)

#### Quick Deploy to Vercel
1. Fork this repository
2. Create a [Supabase](https://supabase.com) project and note the database URL
3. Import your repo to [Vercel](https://vercel.com)
4. Set environment variables in Vercel dashboard:
   - `DATABASE_URL=postgresql://postgres.xxx:password@db.xxx.supabase.co:5432/postgres`
   - `FLASK_ENV=production`
   - `PYTHONPATH=/var/task`
5. Deploy automatically!

The backend runs as Vercel serverless functions at `/api/*` endpoints.

📖 **[Full Deployment Guide](docs/DEPLOYMENT.md)**

## Usage

### For Doctors

1. Navigate to `/submit`
2. Select your name from the dropdown
3. Choose the month
4. Click on calendar dates to mark:
   - Red: Unavailable dates
   - Green: Preferred dates
5. Set your desired number of shifts
6. Submit your preferences

### For Schedulers

1. Navigate to `/admin`
2. Select the month to schedule
3. Click "Generate Schedule" to create an automated schedule
4. Click on any date to manually assign/change doctors
5. Export options:
   - "Export PDF" for a full month calendar
   - Individual ICS buttons for each doctor's calendar file

### Managing Doctors

1. Navigate to `/doctors`
2. Add new doctors with their name and initials
3. Deactivate doctors who are no longer scheduling
4. Reactivate doctors as needed

## Scheduling Algorithm

The scheduler prioritizes:
1. Hard constraints (unavailable dates)
2. Preferred dates
3. Desired shift counts
4. Even distribution of shifts
5. Avoiding consecutive nights (when possible)

## API Endpoints

- `GET /api/doctors` - List all doctors
- `POST /api/doctors` - Add a new doctor
- `DELETE /api/doctors/:id` - Deactivate a doctor
- `POST /api/doctors/:id/activate` - Reactivate a doctor
- `GET /api/preferences?month=YYYY-MM` - Get preferences for a month
- `POST /api/submit` - Submit doctor preferences
- `POST /api/generate?month=YYYY-MM` - Generate schedule
- `GET /api/schedule?month=YYYY-MM` - Get schedule for a month
- `POST /api/schedule/edit` - Edit a single assignment
- `GET /api/export/pdf?month=YYYY-MM` - Export PDF
- `GET /api/export/ics?month=YYYY-MM&doctor=XX` - Export ICS

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `FLASK_ENV`: Set to 'production' for deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License