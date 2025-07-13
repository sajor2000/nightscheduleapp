import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_ENDPOINTS, API_CONFIG } from '../config/api';
import './Doctors.css';

function Doctors() {
  const [doctors, setDoctors] = useState([]);
  const [showInactive, setShowInactive] = useState(false);
  const [newDoctor, setNewDoctor] = useState({ name: '', initials: '' });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('name');

  useEffect(() => {
    loadDoctors();
  }, [showInactive]);

  const loadDoctors = async () => {
    try {
      const response = await axios.get(`${API_ENDPOINTS.doctors}?active=${!showInactive}`, API_CONFIG);
      setDoctors(response.data);
    } catch (error) {
      console.error('Error loading doctors:', error);
      setMessage('Error loading doctors');
    }
  };

  const handleAddDoctor = async (e) => {
    e.preventDefault();
    
    if (!newDoctor.name || !newDoctor.initials) {
      setMessage('Please fill in all fields');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      await axios.post(API_ENDPOINTS.addDoctor, newDoctor, API_CONFIG);
      setNewDoctor({ name: '', initials: '' });
      await loadDoctors();
      setMessage('Doctor added successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      if (error.response?.data?.error) {
        setMessage(error.response.data.error);
      } else {
        setMessage('Error adding doctor');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDeactivate = async (doctorId, doctorName) => {
    if (!window.confirm(`Are you sure you want to deactivate ${doctorName}?`)) {
      return;
    }

    try {
      await axios.delete(API_ENDPOINTS.deleteDoctor(doctorId), API_CONFIG);
      await loadDoctors();
      setMessage(`${doctorName} has been deactivated`);
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Error deactivating doctor');
    }
  };

  const handleActivate = async (doctorId, doctorName) => {
    try {
      await axios.post(API_ENDPOINTS.activateDoctor(doctorId), {}, API_CONFIG);
      await loadDoctors();
      setMessage(`${doctorName} has been activated`);
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Error activating doctor');
    }
  };

  const filteredDoctors = doctors
    .filter(doctor => 
      doctor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      doctor.initials.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      switch(sortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'initials':
          return a.initials.localeCompare(b.initials);
        case 'status':
          return b.active - a.active;
        default:
          return 0;
      }
    });

  const activeCount = doctors.filter(d => d.active).length;
  const inactiveCount = doctors.filter(d => !d.active).length;

  return (
    <div className="doctors-page">
      <div className="page-header">
        <div className="page-header-content">
          <h2>Manage Doctors</h2>
          <p>Add and manage physicians in the MICU rotation</p>
        </div>
      </div>

      <div className="doctors-content">
        <div className="stats-row">
          <div className="mini-stat">
            <span className="stat-value">{activeCount}</span>
            <span className="stat-label">Active Doctors</span>
          </div>
          <div className="mini-stat">
            <span className="stat-value">{inactiveCount}</span>
            <span className="stat-label">Inactive</span>
          </div>
          <div className="mini-stat">
            <span className="stat-value">{doctors.length}</span>
            <span className="stat-label">Total</span>
          </div>
        </div>

        <div className="add-doctor-section">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Add New Doctor</h3>
            </div>
            
            <form onSubmit={handleAddDoctor} className="add-doctor-form">
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">Full Name</label>
                  <input
                    type="text"
                    placeholder="e.g., Dr. Jane Smith"
                    value={newDoctor.name}
                    onChange={(e) => setNewDoctor({ ...newDoctor, name: e.target.value })}
                    className="form-control"
                  />
                </div>
                
                <div className="form-group">
                  <label className="form-label">Initials</label>
                  <input
                    type="text"
                    placeholder="e.g., JS"
                    value={newDoctor.initials}
                    onChange={(e) => setNewDoctor({ ...newDoctor, initials: e.target.value.toUpperCase() })}
                    maxLength="4"
                    className="form-control initials-input"
                  />
                </div>
                
                <button type="submit" disabled={loading} className="btn btn-primary">
                  {loading ? (
                    <>
                      <span className="loading-spinner"></span>
                      Adding...
                    </>
                  ) : (
                    <>
                      <svg className="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                      </svg>
                      Add Doctor
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>

        {message && (
          <div className={`alert ${message.includes('Error') || message.includes('error') ? 'alert-danger' : 'alert-success'} show`}>
            <div className="alert-content">
              {message.includes('Error') || message.includes('error') ? (
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

        <div className="doctors-list-section">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Doctor Directory</h3>
              <div className="table-controls">
                <div className="search-box">
                  <svg className="search-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  <input
                    type="text"
                    placeholder="Search doctors..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="search-input"
                  />
                </div>
                
                <div className="filter-controls">
                  <select 
                    value={sortBy} 
                    onChange={(e) => setSortBy(e.target.value)}
                    className="sort-select"
                  >
                    <option value="name">Sort by Name</option>
                    <option value="initials">Sort by Initials</option>
                    <option value="status">Sort by Status</option>
                  </select>
                  
                  <label className="toggle-switch">
                    <input
                      type="checkbox"
                      checked={showInactive}
                      onChange={(e) => setShowInactive(e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                    <span className="toggle-label">Show Inactive</span>
                  </label>
                </div>
              </div>
            </div>

            <div className="table-wrapper">
              <table className="table doctors-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Initials</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredDoctors.map(doctor => (
                    <tr key={doctor.id} className={!doctor.active ? 'inactive-row' : ''}>
                      <td>
                        <div className="doctor-cell">
                          <div className="doctor-avatar">
                            {doctor.initials}
                          </div>
                          <span className="doctor-name">{doctor.name}</span>
                        </div>
                      </td>
                      <td>
                        <span className="initials-badge">{doctor.initials}</span>
                      </td>
                      <td>
                        <span className={`badge ${doctor.active ? 'badge-success' : 'badge-danger'}`}>
                          {doctor.active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td>
                        <div className="action-buttons">
                          {doctor.active ? (
                            <button 
                              onClick={() => handleDeactivate(doctor.id, doctor.name)}
                              className="btn btn-sm btn-outline-danger"
                              title="Deactivate doctor"
                            >
                              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                              </svg>
                              Deactivate
                            </button>
                          ) : (
                            <button 
                              onClick={() => handleActivate(doctor.id, doctor.name)}
                              className="btn btn-sm btn-outline-success"
                              title="Activate doctor"
                            >
                              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                              </svg>
                              Activate
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {filteredDoctors.length === 0 && (
                <div className="empty-state">
                  <svg className="empty-state-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  <h3>No doctors found</h3>
                  <p>{searchTerm ? 'Try adjusting your search criteria' : 'Add your first doctor to get started'}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Doctors;