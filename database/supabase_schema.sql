-- 🏥 MICU Night Shift Scheduler - Supabase Database Schema
-- This script creates the complete database structure for the MICU Scheduler application
-- Compatible with Supabase PostgreSQL

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Clean setup: Drop existing tables if they exist
DROP TABLE IF EXISTS schedule CASCADE;
DROP TABLE IF EXISTS preferences CASCADE; 
DROP TABLE IF EXISTS doctors CASCADE;

-- =============================================================================
-- DOCTORS TABLE
-- Stores all physicians in the MICU rotation
-- =============================================================================
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL CHECK (length(name) > 0),
    initials TEXT UNIQUE NOT NULL CHECK (length(initials) BETWEEN 2 AND 4),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================================================
-- PREFERENCES TABLE  
-- Stores monthly availability preferences submitted by doctors
-- =============================================================================
CREATE TABLE preferences (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    month TEXT NOT NULL CHECK (month ~ '^\d{4}-\d{2}$'), -- Format: YYYY-MM
    unavailable TEXT[] DEFAULT '{}', -- Array of dates in YYYY-MM-DD format
    preferred TEXT[] DEFAULT '{}',   -- Array of dates in YYYY-MM-DD format
    desired_shifts INTEGER NOT NULL DEFAULT 7 CHECK (desired_shifts >= 0 AND desired_shifts <= 31),
    submitted_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Ensure one preference record per doctor per month
    UNIQUE(doctor_id, month)
);

-- =============================================================================
-- SCHEDULE TABLE
-- Stores the final generated/edited schedule assignments
-- =============================================================================
CREATE TABLE schedule (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    month TEXT NOT NULL CHECK (month ~ '^\d{4}-\d{2}$'), -- Format: YYYY-MM
    created_at TIMESTAMPTZ DEFAULT NOW(),
    modified_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Each date can only have one doctor assigned
    UNIQUE(date)
);

-- =============================================================================
-- PERFORMANCE INDEXES
-- Optimize common query patterns
-- =============================================================================
CREATE INDEX idx_doctors_active ON doctors(active) WHERE active = true;
CREATE INDEX idx_doctors_initials ON doctors(initials);

CREATE INDEX idx_preferences_month ON preferences(month);
CREATE INDEX idx_preferences_doctor_month ON preferences(doctor_id, month);

CREATE INDEX idx_schedule_month ON schedule(month);
CREATE INDEX idx_schedule_date ON schedule(date);
CREATE INDEX idx_schedule_doctor_month ON schedule(doctor_id, month);

-- =============================================================================
-- TRIGGERS FOR AUTOMATIC TIMESTAMPS
-- =============================================================================
CREATE OR REPLACE FUNCTION update_modified_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER schedule_update_modified_at
    BEFORE UPDATE ON schedule
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_at();

-- =============================================================================
-- DATA VALIDATION FUNCTIONS
-- =============================================================================
CREATE OR REPLACE FUNCTION validate_date_format(date_array TEXT[])
RETURNS BOOLEAN AS $$
BEGIN
    -- Check that all dates in array are valid YYYY-MM-DD format
    RETURN (
        SELECT COALESCE(
            bool_and(date_text ~ '^\d{4}-\d{2}-\d{2}$' AND date_text::DATE IS NOT NULL),
            true
        )
        FROM unnest(date_array) AS date_text
    );
END;
$$ LANGUAGE plpgsql;

-- Add validation constraints
ALTER TABLE preferences 
ADD CONSTRAINT preferences_unavailable_format_check 
CHECK (validate_date_format(unavailable));

ALTER TABLE preferences 
ADD CONSTRAINT preferences_preferred_format_check 
CHECK (validate_date_format(preferred));

-- =============================================================================
-- INITIAL DATA: RUSH UNIVERSITY MEDICAL CENTER MICU DOCTORS
-- These are the 25 physicians who work in the MICU night rotation
-- =============================================================================
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

-- =============================================================================
-- VERIFICATION QUERIES
-- Run these to verify the setup worked correctly
-- =============================================================================

-- Should return 25 active doctors
-- SELECT COUNT(*) as total_doctors, COUNT(*) FILTER (WHERE active) as active_doctors FROM doctors;

-- Should show all doctor names and initials
-- SELECT name, initials, active FROM doctors ORDER BY name;

-- Should return empty results (no preferences/schedules yet)
-- SELECT COUNT(*) as total_preferences FROM preferences;
-- SELECT COUNT(*) as total_scheduled_shifts FROM schedule;

-- =============================================================================
-- SETUP COMPLETE!
-- =============================================================================

-- Success message
DO $$
BEGIN
    RAISE NOTICE '🎉 MICU Scheduler database setup completed successfully!';
    RAISE NOTICE '📊 Created % doctors in the system', (SELECT COUNT(*) FROM doctors);
    RAISE NOTICE '✅ All tables, indexes, and constraints are ready';
    RAISE NOTICE '🚀 Your Supabase database is ready for the MICU Scheduler app!';
END $$;