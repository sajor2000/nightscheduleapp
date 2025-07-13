-- 🌱 MICU Scheduler - Test Data Seeding Script
-- This script adds sample data for development and testing
-- Run this AFTER the main schema (supabase_schema.sql)

-- =============================================================================
-- SAMPLE PREFERENCES FOR CURRENT MONTH
-- Add realistic preference data for testing the scheduling algorithm
-- =============================================================================

-- Get current month in YYYY-MM format for consistent testing
DO $$
DECLARE
    current_month TEXT := TO_CHAR(CURRENT_DATE, 'YYYY-MM');
BEGIN
    RAISE NOTICE 'Adding sample preferences for month: %', current_month;
    
    -- Sample preferences for various doctors with different patterns
    INSERT INTO preferences (doctor_id, month, unavailable, preferred, desired_shifts) VALUES
    
    -- Dr. Akshay Kohli (AK) - Prefers beginning of month, unavailable mid-month
    (1, current_month, 
     ARRAY[current_month || '-15', current_month || '-16', current_month || '-17'], 
     ARRAY[current_month || '-01', current_month || '-02', current_month || '-03'], 
     7),
    
    -- Dr. Amie Gamino (AG) - High availability, wants many shifts
    (2, current_month, 
     ARRAY[current_month || '-25'], 
     ARRAY[current_month || '-05', current_month || '-10', current_month || '-20', current_month || '-21'], 
     10),
    
    -- Dr. Abhaya Trivedi (AT) - Limited availability, fewer shifts
    (3, current_month, 
     ARRAY[current_month || '-01', current_month || '-02', current_month || '-03', current_month || '-28', current_month || '-29'], 
     ARRAY[current_month || '-12', current_month || '-13'], 
     5),
    
    -- Dr. Babak Mokhlesi (BM) - Weekend preferences
    (4, current_month, 
     ARRAY[current_month || '-08', current_month || '-09'], 
     ARRAY[current_month || '-06', current_month || '-07', current_month || '-14'], 
     8),
    
    -- Dr. Brian Stein (BS) - Regular schedule
    (5, current_month, 
     ARRAY[current_month || '-20', current_month || '-21', current_month || '-22'], 
     ARRAY[current_month || '-04', current_month || '-11', current_month || '-18'], 
     7),
    
    -- Dr. David Gurka (DG) - Flexible schedule
    (6, current_month, 
     ARRAY[current_month || '-30'], 
     ARRAY[current_month || '-08', current_month || '-09', current_month || '-16', current_month || '-23'], 
     9),
    
    -- Dr. Elaine Chen (EC) - End of month unavailable
    (7, current_month, 
     ARRAY[current_month || '-26', current_month || '-27', current_month || '-28', current_month || '-29'], 
     ARRAY[current_month || '-05', current_month || '-12'], 
     6),
    
    -- Dr. Ed Pickering (EP) - Mid-month focus
    (8, current_month, 
     ARRAY[current_month || '-01', current_month || '-31'], 
     ARRAY[current_month || '-15', current_month || '-16', current_month || '-17'], 
     8),
    
    -- Dr. JC Rojas (JCR) - Consistent availability
    (9, current_month, 
     ARRAY[current_month || '-10', current_month || '-11'], 
     ARRAY[current_month || '-07', current_month || '-14', current_month || '-21', current_month || '-28'], 
     8),
    
    -- Dr. Jessica Kuppy (JEK) - Lower shift count
    (10, current_month, 
     ARRAY[current_month || '-05', current_month || '-06', current_month || '-19', current_month || '-20'], 
     ARRAY[current_month || '-13', current_month || '-27'], 
     5);

END $$;

-- =============================================================================
-- SAMPLE SCHEDULE DATA 
-- Add some pre-generated schedule entries for testing exports
-- =============================================================================

DO $$
DECLARE
    current_month TEXT := TO_CHAR(CURRENT_DATE, 'YYYY-MM');
    sample_date DATE;
BEGIN
    RAISE NOTICE 'Adding sample schedule for month: %', current_month;
    
    -- Add some sample scheduled shifts
    INSERT INTO schedule (doctor_id, date, month) VALUES
    (1, (current_month || '-01')::DATE, current_month),
    (2, (current_month || '-02')::DATE, current_month),
    (3, (current_month || '-03')::DATE, current_month),
    (4, (current_month || '-04')::DATE, current_month),
    (5, (current_month || '-05')::DATE, current_month),
    (6, (current_month || '-06')::DATE, current_month),
    (7, (current_month || '-07')::DATE, current_month),
    (8, (current_month || '-08')::DATE, current_month),
    (9, (current_month || '-09')::DATE, current_month),
    (10, (current_month || '-10')::DATE, current_month);

END $$;

-- =============================================================================
-- PREFERENCE DATA FOR NEXT MONTH
-- Allow testing of future month scheduling
-- =============================================================================

DO $$
DECLARE
    next_month TEXT := TO_CHAR(CURRENT_DATE + INTERVAL '1 month', 'YYYY-MM');
BEGIN
    RAISE NOTICE 'Adding sample preferences for next month: %', next_month;
    
    -- Add fewer preferences for next month to test partial submissions
    INSERT INTO preferences (doctor_id, month, unavailable, preferred, desired_shifts) VALUES
    (1, next_month, 
     ARRAY[next_month || '-10', next_month || '-11'], 
     ARRAY[next_month || '-01', next_month || '-15'], 
     6),
    (5, next_month, 
     ARRAY[next_month || '-20'], 
     ARRAY[next_month || '-05', next_month || '-12'], 
     7),
    (9, next_month, 
     ARRAY[next_month || '-25', next_month || '-26'], 
     ARRAY[next_month || '-08', next_month || '-22'], 
     8);

END $$;

-- =============================================================================
-- VERIFICATION AND STATISTICS
-- =============================================================================

-- Display summary of seeded data
DO $$
DECLARE
    doctor_count INTEGER;
    preference_count INTEGER;
    schedule_count INTEGER;
    current_month TEXT := TO_CHAR(CURRENT_DATE, 'YYYY-MM');
BEGIN
    SELECT COUNT(*) INTO doctor_count FROM doctors WHERE active = true;
    SELECT COUNT(*) INTO preference_count FROM preferences;
    SELECT COUNT(*) INTO schedule_count FROM schedule;
    
    RAISE NOTICE '';
    RAISE NOTICE '=== SEEDING COMPLETE ===';
    RAISE NOTICE 'Active doctors: %', doctor_count;
    RAISE NOTICE 'Total preferences: %', preference_count;
    RAISE NOTICE 'Scheduled shifts: %', schedule_count;
    RAISE NOTICE '';
    RAISE NOTICE 'Current month (%) has % doctors with preferences', current_month, 
                 (SELECT COUNT(*) FROM preferences WHERE month = current_month);
    RAISE NOTICE '';
    RAISE NOTICE '🎯 Ready to test:';
    RAISE NOTICE '   • Doctor management (add/deactivate)';
    RAISE NOTICE '   • Preference submission';
    RAISE NOTICE '   • Schedule generation'; 
    RAISE NOTICE '   • PDF/ICS exports';
    RAISE NOTICE '';
END $$;

-- =============================================================================
-- SAMPLE QUERIES FOR TESTING
-- Uncomment and run these to verify the data looks correct
-- =============================================================================

/*
-- View doctors with preferences
SELECT 
    d.name,
    d.initials,
    p.month,
    array_length(p.unavailable, 1) as unavailable_days,
    array_length(p.preferred, 1) as preferred_days,
    p.desired_shifts
FROM doctors d
JOIN preferences p ON d.id = p.doctor_id
ORDER BY d.name, p.month;

-- View current schedule
SELECT 
    s.date,
    d.name,
    d.initials,
    s.month
FROM schedule s
JOIN doctors d ON s.doctor_id = d.id
ORDER BY s.date;

-- Summary by month
SELECT 
    month,
    COUNT(*) as doctors_with_preferences,
    AVG(desired_shifts) as avg_desired_shifts,
    SUM(array_length(unavailable, 1)) as total_unavailable_days
FROM preferences
GROUP BY month
ORDER BY month;
*/