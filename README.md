# MICU Night Shift Scheduler

A web application for scheduling night shifts for physicians at Rush University Medical Center's Medical Intensive Care Unit (MICU).

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

### Deployment on Replit

1. Fork/import this repository to Replit
2. The application will automatically:
   - Install dependencies
   - Initialize the database
   - Build the React frontend
   - Start the Flask server

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