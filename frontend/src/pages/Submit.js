import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import axios from 'axios';
import './Submit.css';

function Submit() {
  const [doctors, setDoctors] = useState([]);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [selectedMonth, setSelectedMonth] = useState('');
  const [unavailableDates, setUnavailableDates] = useState([]);
  const [preferredDates, setPreferredDates] = useState([]);
  const [desiredShifts, setDesiredShifts] = useState(7);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    fetchDoctors();
    
    const today = new Date();
    const nextMonth = new Date(today.getFullYear(), today.getMonth() + 1);
    const monthStr = `${nextMonth.getFullYear()}-${String(nextMonth.getMonth() + 1).padStart(2, '0')}`;
    setSelectedMonth(monthStr);
  }, []);

  const fetchDoctors = async () => {
    try {
      const response = await axios.get('/api/doctors');
      const options = response.data.map(doc => ({
        value: doc.id,
        label: `${doc.name} (${doc.initials})`
      }));
      setDoctors(options);
    } catch (error) {
      console.error('Error fetching doctors:', error);
    }
  };

  const handleDateClick = (info) => {
    const dateStr = info.dateStr;
    
    if (unavailableDates.includes(dateStr)) {
      setUnavailableDates(unavailableDates.filter(d => d !== dateStr));
      setPreferredDates([...preferredDates, dateStr]);
    } else if (preferredDates.includes(dateStr)) {
      setPreferredDates(preferredDates.filter(d => d !== dateStr));
    } else {
      setUnavailableDates([...unavailableDates, dateStr]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedDoctor) {
      setMessage('Please select a doctor');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      await axios.post('/api/submit', {
        doctor_id: selectedDoctor.value,
        month: selectedMonth,
        unavailable: unavailableDates,
        preferred: preferredDates,
        desired_shifts: desiredShifts
      });

      setShowSuccess(true);
      setMessage('Preferences submitted successfully!');
      
      // Reset form after delay
      setTimeout(() => {
        setUnavailableDates([]);
        setPreferredDates([]);
        setDesiredShifts(7);
        setShowSuccess(false);
      }, 3000);
    } catch (error) {
      setMessage('Error submitting preferences. Please try again.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getEventDisplay = () => {
    const events = [];
    
    unavailableDates.forEach(date => {
      events.push({
        date: date,
        title: 'Cannot Work',
        backgroundColor: '#DC3545',
        borderColor: '#DC3545',
        textColor: '#FFFFFF'
      });
    });
    
    preferredDates.forEach(date => {
      events.push({
        date: date,
        title: 'Prefer to Work',
        backgroundColor: '#28A745',
        borderColor: '#28A745',
        textColor: '#FFFFFF'
      });
    });
    
    return events;
  };

  const customSelectStyles = {
    control: (provided, state) => ({
      ...provided,
      borderColor: state.isFocused ? 'var(--rush-green)' : 'var(--gray-300)',
      boxShadow: state.isFocused ? '0 0 0 0.2rem rgba(0, 87, 63, 0.25)' : 'none',
      '&:hover': {
        borderColor: 'var(--rush-green)'
      }
    }),
    option: (provided, state) => ({
      ...provided,
      backgroundColor: state.isSelected ? 'var(--rush-green)' : state.isFocused ? 'var(--gray-100)' : 'white',
      color: state.isSelected ? 'white' : 'var(--gray-800)',
      '&:hover': {
        backgroundColor: state.isSelected ? 'var(--rush-green)' : 'var(--gray-100)'
      }
    })
  };

  return (
    <div className="submit-page">
      <div className="page-header">
        <div className="page-header-content">
          <h2>Submit Monthly Availability</h2>
          <p>Select your availability preferences for night shifts</p>
        </div>
      </div>
      
      <div className="submit-content">
        <form onSubmit={handleSubmit} className="submit-form">
          <div className="form-section">
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Basic Information</h3>
              </div>
              
              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Doctor Name</label>
                  <Select
                    value={selectedDoctor}
                    onChange={setSelectedDoctor}
                    options={doctors}
                    placeholder="Select your name..."
                    isSearchable
                    styles={customSelectStyles}
                    className="doctor-select"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Month</label>
                  <input
                    type="month"
                    value={selectedMonth}
                    onChange={(e) => setSelectedMonth(e.target.value)}
                    className="form-control"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Desired Number of Shifts</label>
                  <div className="shift-input-wrapper">
                    <input
                      type="number"
                      value={desiredShifts}
                      onChange={(e) => setDesiredShifts(parseInt(e.target.value) || 0)}
                      min="0"
                      max="31"
                      className="form-control"
                    />
                    <span className="shift-label">nights</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="form-section">
            <div className="card calendar-card">
              <div className="card-header">
                <h3 className="card-title">Select Your Availability</h3>
                <div className="legend">
                  <div className="legend-item">
                    <span className="legend-color unavailable"></span>
                    <span>Cannot Work</span>
                  </div>
                  <div className="legend-item">
                    <span className="legend-color preferred"></span>
                    <span>Prefer to Work</span>
                  </div>
                  <div className="legend-item">
                    <span className="legend-color neutral"></span>
                    <span>Available</span>
                  </div>
                </div>
              </div>
              
              <div className="calendar-wrapper">
                <FullCalendar
                  plugins={[dayGridPlugin, interactionPlugin]}
                  initialView="dayGridMonth"
                  initialDate={`${selectedMonth}-01`}
                  dateClick={handleDateClick}
                  events={getEventDisplay()}
                  height="auto"
                  headerToolbar={{
                    left: '',
                    center: 'title',
                    right: ''
                  }}
                  dayMaxEvents={1}
                  eventDisplay="block"
                />
              </div>
              
              <div className="calendar-footer">
                <p className="help-text">
                  <svg className="help-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Click on dates to cycle through: Unavailable → Preferred → Available
                </p>
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button 
              type="submit" 
              disabled={loading}
              className={`btn btn-primary btn-lg ${loading ? 'loading' : ''}`}
            >
              {loading ? (
                <>
                  <span className="loading-spinner"></span>
                  Submitting...
                </>
              ) : (
                <>
                  <svg className="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Submit Preferences
                </>
              )}
            </button>
          </div>

          {message && (
            <div className={`alert ${message.includes('Error') ? 'alert-danger' : 'alert-success'} ${showSuccess ? 'show' : ''}`}>
              <div className="alert-content">
                {message.includes('Error') ? (
                  <svg className="alert-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                ) : (
                  <svg className="alert-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                )}
                <span>{message}</span>
              </div>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

export default Submit;