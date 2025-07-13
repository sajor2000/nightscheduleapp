-- MICU Night Shift Scheduler Database Schema

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS schedule CASCADE;
DROP TABLE IF EXISTS preferences CASCADE;
DROP TABLE IF EXISTS doctors CASCADE;

-- Doctors table
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    initials TEXT UNIQUE NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Preferences table
CREATE TABLE preferences (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    month TEXT NOT NULL, -- Format: YYYY-MM
    unavailable TEXT[] DEFAULT '{}', -- Array of dates (YYYY-MM-DD)
    preferred TEXT[] DEFAULT '{}', -- Array of dates (YYYY-MM-DD)
    desired_shifts INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(doctor_id, month)
);

-- Schedule table
CREATE TABLE schedule (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    month TEXT NOT NULL, -- Format: YYYY-MM
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(date)
);

-- Create indexes for better performance
CREATE INDEX idx_schedule_month ON schedule(month);
CREATE INDEX idx_schedule_date ON schedule(date);
CREATE INDEX idx_preferences_month ON preferences(month);
CREATE INDEX idx_doctors_active ON doctors(active);

-- Insert initial doctor list
INSERT INTO doctors (name, initials) VALUES
    ('Akshay Kohli', 'AK'),
    ('Amie Gamino', 'AG'),
    ('Abhaya Trivedi', 'AT'),
    ('Babak Mokhlesi', 'BM'),
    ('Brian Stein', 'BS'),
    ('David Gurka', 'DG'),
    ('Elaine Chen', 'EC'),
    ('Ed Pickering', 'EP'),
    ('JC Rojas', 'JCR'),
    ('Jessica Kuppy', 'JEK'),
    ('Jared Greenberg', 'JG'),
    ('James Katsis', 'JK'),
    ('Julie Neborak', 'JN'),
    ('James Rowley', 'JR'),
    ('Kevin Buell', 'KB'),
    ('Kari Jackson', 'KJ'),
    ('Kalli Sarigiannis', 'KS'),
    ('Meghan Snuckel', 'MS'),
    ('Mark Tancredi', 'MT'),
    ('Mona Vashi', 'MV'),
    ('Mark Yoder', 'MY'),
    ('Prema Nanavaty', 'PN'),
    ('Sam Fox', 'SF'),
    ('Shruti Patel', 'SP'),
    ('Waj Lodhi', 'WL');

-- Sample preferences for current month
INSERT INTO preferences (doctor_id, month, unavailable, preferred, desired_shifts) VALUES
    (1, '2025-08', ARRAY['2025-08-10', '2025-08-11', '2025-08-12'], ARRAY['2025-08-01', '2025-08-02'], 7),
    (2, '2025-08', ARRAY['2025-08-15', '2025-08-16'], ARRAY['2025-08-20', '2025-08-21', '2025-08-22'], 8),
    (3, '2025-08', ARRAY['2025-08-01', '2025-08-02', '2025-08-03'], ARRAY['2025-08-25', '2025-08-26'], 6);