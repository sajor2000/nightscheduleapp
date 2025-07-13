import React, { useState, useEffect } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import Select from 'react-select';
import axios from 'axios';
import './Admin.css';

function Admin() {
  const [selectedMonth, setSelectedMonth] = useState('');
  const [preferences, setPreferences] = useState([]);
  const [schedule, setSchedule] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [editingDate, setEditingDate] = useState(null);
  const [stats, setStats] = useState({ total: 0, assigned: 0, coverage: 0 });

  useEffect(() => {
    const today = new Date();
    const monthStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`;
    setSelectedMonth(monthStr);
    
    fetchDoctors();
  }, []);

  useEffect(() => {
    if (selectedMonth) {
      loadMonthData();
    }
  }, [selectedMonth]);

  const fetchDoctors = async () => {
    try {
      const response = await axios.get('/api/doctors');
      setDoctors(response.data);
    } catch (error) {
      console.error('Error fetching doctors:', error);
    }
  };

  const loadMonthData = async () => {
    setLoading(true);
    try {
      const [prefResponse, schedResponse] = await Promise.all([
        axios.get(`/api/preferences?month=${selectedMonth}`),
        axios.get(`/api/schedule?month=${selectedMonth}`)
      ]);
      
      setPreferences(prefResponse.data);
      setSchedule(schedResponse.data);
      
      // Calculate stats
      const daysInMonth = new Date(
        parseInt(selectedMonth.split('-')[0]),
        parseInt(selectedMonth.split('-')[1]),
        0
      ).getDate();
      
      setStats({
        total: daysInMonth,
        assigned: schedResponse.data.length,
        coverage: Math.round((schedResponse.data.length / daysInMonth) * 100)
      });
    } catch (error) {
      console.error('Error loading data:', error);
      setMessage('Error loading data');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSchedule = async () => {
    if (!window.confirm('Generate new schedule? This will overwrite any manual edits.')) {
      return;
    }

    setLoading(true);
    setMessage('');
    
    try {
      await axios.post(`/api/generate?month=${selectedMonth}`);
      await loadMonthData();
      setMessage('Schedule generated successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      console.error('Error generating schedule:', error);
      setMessage('Error generating schedule. Check that all doctors have submitted preferences.');
    } finally {
      setLoading(false);
    }
  };

  const handleDateClick = (info) => {
    setEditingDate(info.dateStr);
  };

  const handleAssignDoctor = async (doctorId) => {
    if (!editingDate) return;

    try {
      await axios.post('/api/schedule/edit', {
        date: editingDate,
        doctor_id: doctorId
      });
      
      await loadMonthData();
      setEditingDate(null);
      setMessage('Schedule updated');
      setTimeout(() => setMessage(''), 2000);
    } catch (error) {
      console.error('Error updating schedule:', error);
      setMessage('Error updating schedule');
    }
  };

  const handleExportPDF = () => {
    window.open(`/api/export/pdf?month=${selectedMonth}`, '_blank');
  };

  const handleExportICS = (doctorInitials) => {
    window.open(`/api/export/ics?month=${selectedMonth}&doctor=${doctorInitials}`, '_blank');
  };

  const getCalendarEvents = () => {
    const events = [];
    
    schedule.forEach(shift => {
      events.push({
        date: shift.date,
        title: shift.doctor_initials,
        backgroundColor: 'var(--rush-green)',
        borderColor: 'var(--rush-dark-green)',
        textColor: 'var(--white)',
        classNames: ['scheduled-shift']
      });
    });
    
    return events;
  };

  const getPreferenceSummary = () => {
    const summary = {};
    
    preferences.forEach(pref => {
      summary[pref.doctor_id] = {
        name: pref.doctor_name,
        initials: pref.doctor_initials,
        desired: pref.desired_shifts,
        assigned: schedule.filter(s => s.doctor_id === pref.doctor_id).length,
        unavailable: pref.unavailable.length,
        preferred: pref.preferred.length
      };
    });
    
    return Object.values(summary);
  };

  const getMonthName = () => {
    if (!selectedMonth) return '';
    const [year, month] = selectedMonth.split('-');
    const date = new Date(year, month - 1);
    return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  };

  return (
    <div className="admin-page">
      <div className="page-header">
        <div className="page-header-content">
          <h2>Admin Dashboard</h2>
          <p>Manage and optimize the MICU night shift schedule</p>
        </div>
      </div>
      
      <div className="admin-content">
        <div className="stats-section">
          <div className="stat-card">
            <div className="stat-icon">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div className="stat-content">
              <h3>{stats.total}</h3>
              <p>Total Days</p>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="stat-icon assigned">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="stat-content">
              <h3>{stats.assigned}</h3>
              <p>Assigned Shifts</p>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="stat-icon coverage">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div className="stat-content">
              <h3>{stats.coverage}%</h3>
              <p>Coverage Rate</p>
            </div>
          </div>
        </div>

        <div className="controls-section">
          <div className="card">
            <div className="controls-grid">
              <div className="control-group">
                <label className="form-label">Schedule Month</label>
                <input
                  type="month"
                  value={selectedMonth}
                  onChange={(e) => setSelectedMonth(e.target.value)}
                  className="form-control"
                />
              </div>
              
              <div className="control-actions">
                <button 
                  onClick={handleGenerateSchedule}
                  disabled={loading || preferences.length === 0}
                  className="btn btn-primary"
                >
                  <svg className="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  Generate Schedule
                </button>
                
                <button 
                  onClick={handleExportPDF}
                  disabled={schedule.length === 0}
                  className="btn btn-secondary"
                >
                  <svg className="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                  Export PDF
                </button>
              </div>
            </div>
          </div>
        </div>

        {message && (
          <div className={`alert ${message.includes('Error') ? 'alert-danger' : 'alert-success'} show`}>
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

        <div className="dashboard-grid">
          <div className="calendar-section">
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">
                  {getMonthName()} Schedule
                </h3>
                <p className="card-subtitle">Click any date to assign or modify</p>
              </div>
              
              <div className="calendar-wrapper">
                <FullCalendar
                  plugins={[dayGridPlugin, interactionPlugin]}
                  initialView="dayGridMonth"
                  initialDate={`${selectedMonth}-01`}
                  dateClick={handleDateClick}
                  events={getCalendarEvents()}
                  height="auto"
                  headerToolbar={{
                    left: '',
                    center: '',
                    right: ''
                  }}
                  dayMaxEvents={1}
                  eventDisplay="block"
                />
              </div>
            </div>
          </div>

          <div className="sidebar">
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Doctor Summary</h3>
              </div>
              
              <div className="summary-table">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Doctor</th>
                      <th>Target</th>
                      <th>Actual</th>
                      <th>Status</th>
                      <th>ICS</th>
                    </tr>
                  </thead>
                  <tbody>
                    {getPreferenceSummary().map(doc => {
                      const diff = doc.assigned - doc.desired;
                      const status = diff === 0 ? 'optimal' : diff > 0 ? 'over' : 'under';
                      
                      return (
                        <tr key={doc.initials}>
                          <td>
                            <div className="doctor-info">
                              <span className="doctor-initials">{doc.initials}</span>
                              <span className="doctor-name">{doc.name}</span>
                            </div>
                          </td>
                          <td className="text-center">{doc.desired}</td>
                          <td className="text-center">{doc.assigned}</td>
                          <td>
                            <span className={`status-indicator ${status}`}>
                              {diff === 0 ? '✓' : diff > 0 ? `+${diff}` : diff}
                            </span>
                          </td>
                          <td>
                            <button 
                              onClick={() => handleExportICS(doc.initials)}
                              className="btn-icon-only"
                              title="Download calendar file"
                            >
                              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                              </svg>
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
              
              {preferences.length === 0 && (
                <div className="empty-state">
                  <p>No preferences submitted for this month</p>
                </div>
              )}
            </div>
            
            {editingDate && (
              <div className="card edit-panel">
                <div className="card-header">
                  <h3 className="card-title">Assign Doctor</h3>
                  <button onClick={() => setEditingDate(null)} className="close-button">
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                
                <p className="edit-date">{new Date(editingDate).toLocaleDateString('en-US', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}</p>
                
                <div className="doctor-list">
                  {doctors.map(doc => {
                    const pref = preferences.find(p => p.doctor_id === doc.id);
                    const isUnavailable = pref?.unavailable.includes(editingDate);
                    const isPreferred = pref?.preferred.includes(editingDate);
                    
                    return (
                      <button
                        key={doc.id}
                        onClick={() => handleAssignDoctor(doc.id)}
                        className={`doctor-option ${isUnavailable ? 'unavailable' : ''} ${isPreferred ? 'preferred' : ''}`}
                        disabled={isUnavailable}
                      >
                        <span className="doctor-option-name">{doc.name}</span>
                        <span className="doctor-option-initials">({doc.initials})</span>
                        {isUnavailable && <span className="status-tag">Unavailable</span>}
                        {isPreferred && <span className="status-tag preferred">Preferred</span>}
                      </button>
                    );
                  })}
                  
                  <button
                    onClick={() => handleAssignDoctor(null)}
                    className="doctor-option remove"
                  >
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Remove Assignment
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Admin;