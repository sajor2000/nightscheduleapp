// API Configuration for Vercel + Supabase deployment

// For Vercel deployment, API endpoints are serverless functions
const IS_DEVELOPMENT = process.env.REACT_APP_ENVIRONMENT === 'development';
const API_BASE_URL = IS_DEVELOPMENT 
  ? 'http://localhost:3000'  // Development uses Vercel dev server
  : window.location.origin;  // Production uses same domain

const ENVIRONMENT = process.env.REACT_APP_ENVIRONMENT || 'development';

// API endpoints configuration
export const API_CONFIG = {
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
};

// API endpoints for Vercel serverless functions
export const API_ENDPOINTS = {
  // Doctor endpoints
  doctors: `${API_BASE_URL}/api/doctors`,
  addDoctor: `${API_BASE_URL}/api/doctors`,
  deleteDoctor: (id) => `${API_BASE_URL}/api/doctors/delete?id=${id}`,
  activateDoctor: (id) => `${API_BASE_URL}/api/doctors/activate?id=${id}`,
  
  // Preference endpoints
  preferences: (month) => `${API_BASE_URL}/api/preferences?month=${month}`,
  submitPreferences: `${API_BASE_URL}/api/submit`,
  
  // Schedule endpoints
  generateSchedule: (month) => `${API_BASE_URL}/api/generate?month=${month}`,
  getSchedule: (month) => `${API_BASE_URL}/api/schedule?month=${month}`,
  editSchedule: `${API_BASE_URL}/api/schedule/edit`,
  
  // Export endpoints
  exportICS: (month, doctor) => `${API_BASE_URL}/api/export/ics?month=${month}&doctor=${doctor}`,
  exportPDF: (month) => `${API_BASE_URL}/api/export/pdf?month=${month}`,
  
  // Health check
  health: `${API_BASE_URL}/api/health`,
};

// Development helpers
export const isDevelopment = ENVIRONMENT === 'development';
export const isProduction = ENVIRONMENT === 'production';

// Console logging for development
if (isDevelopment) {
  console.log('🏥 MICU Scheduler API Config:', {
    baseURL: API_BASE_URL,
    environment: ENVIRONMENT,
  });
}

export default API_CONFIG;