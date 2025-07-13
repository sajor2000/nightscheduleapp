-- 🔍 MICU Scheduler - Database Verification Queries
-- Run these queries in Supabase SQL Editor to verify everything is working correctly

-- =============================================================================
-- BASIC SETUP VERIFICATION
-- =============================================================================

-- 1. Check all tables exist and have correct structure
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables 
WHERE tablename IN ('doctors', 'preferences', 'schedule')
ORDER BY tablename;

-- 2. Verify doctor data is loaded correctly
SELECT 
    COUNT(*) as total_doctors,
    COUNT(*) FILTER (WHERE active = true) as active_doctors,
    COUNT(*) FILTER (WHERE active = false) as inactive_doctors
FROM doctors;

-- 3. Check that all expected doctors are present
SELECT 
    name,
    initials,
    active,
    created_at
FROM doctors 
ORDER BY name;

-- =============================================================================
-- TABLE STRUCTURE VERIFICATION
-- =============================================================================

-- 4. Verify doctors table structure
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'doctors'
ORDER BY ordinal_position;

-- 5. Verify preferences table structure
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'preferences'
ORDER BY ordinal_position;

-- 6. Verify schedule table structure  
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'schedule'
ORDER BY ordinal_position;

-- =============================================================================
-- CONSTRAINT AND INDEX VERIFICATION
-- =============================================================================

-- 7. Check foreign key constraints
SELECT
    tc.table_name,
    tc.constraint_name,
    tc.constraint_type,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
LEFT JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.table_name IN ('doctors', 'preferences', 'schedule')
    AND tc.constraint_type IN ('FOREIGN KEY', 'UNIQUE', 'PRIMARY KEY')
ORDER BY tc.table_name, tc.constraint_type;

-- 8. Verify indexes exist
SELECT
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename IN ('doctors', 'preferences', 'schedule')
ORDER BY tablename, indexname;

-- =============================================================================
-- DATA INTEGRITY CHECKS
-- =============================================================================

-- 9. Check for any data integrity issues
-- All doctor IDs in preferences should reference valid doctors
SELECT 
    p.doctor_id,
    d.name
FROM preferences p
LEFT JOIN doctors d ON p.doctor_id = d.id
WHERE d.id IS NULL;

-- 10. All doctor IDs in schedule should reference valid doctors
SELECT 
    s.doctor_id,
    d.name
FROM schedule s
LEFT JOIN doctors d ON s.doctor_id = d.id
WHERE d.id IS NULL;

-- 11. Check month format consistency
SELECT DISTINCT month
FROM preferences
WHERE month !~ '^\d{4}-\d{2}$'
UNION
SELECT DISTINCT month
FROM schedule
WHERE month !~ '^\d{4}-\d{2}$';

-- =============================================================================
-- FUNCTIONAL VERIFICATION
-- =============================================================================

-- 12. Test date array functionality (should work without errors)
SELECT 
    doctor_id,
    month,
    unavailable,
    preferred,
    array_length(unavailable, 1) as unavailable_count,
    array_length(preferred, 1) as preferred_count
FROM preferences
WHERE array_length(unavailable, 1) > 0 OR array_length(preferred, 1) > 0
LIMIT 5;

-- 13. Test date operations (should work without errors)
SELECT 
    date,
    EXTRACT(year FROM date) as year,
    EXTRACT(month FROM date) as month,
    EXTRACT(day FROM date) as day,
    TO_CHAR(date, 'YYYY-MM-DD') as formatted_date
FROM schedule
LIMIT 5;

-- =============================================================================
-- PERFORMANCE VERIFICATION
-- =============================================================================

-- 14. Test common query patterns that the app will use

-- Get active doctors (should be fast with index)
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM doctors WHERE active = true ORDER BY name;

-- Get preferences for a month (should be fast with index)
EXPLAIN (ANALYZE, BUFFERS)
SELECT p.*, d.name, d.initials
FROM preferences p
JOIN doctors d ON p.doctor_id = d.id
WHERE p.month = TO_CHAR(CURRENT_DATE, 'YYYY-MM');

-- Get schedule for a month (should be fast with index)
EXPLAIN (ANALYZE, BUFFERS)
SELECT s.*, d.name, d.initials
FROM schedule s
JOIN doctors d ON s.doctor_id = d.id
WHERE s.month = TO_CHAR(CURRENT_DATE, 'YYYY-MM')
ORDER BY s.date;

-- =============================================================================
-- SUMMARY REPORT
-- =============================================================================

-- 15. Generate final verification summary
WITH summary AS (
    SELECT 
        (SELECT COUNT(*) FROM doctors) as total_doctors,
        (SELECT COUNT(*) FROM doctors WHERE active = true) as active_doctors,
        (SELECT COUNT(*) FROM preferences) as total_preferences,
        (SELECT COUNT(DISTINCT month) FROM preferences) as months_with_preferences,
        (SELECT COUNT(*) FROM schedule) as total_scheduled_shifts,
        (SELECT COUNT(DISTINCT month) FROM schedule) as months_with_schedule
)
SELECT 
    '🏥 MICU Scheduler Database Verification Report' as report_title,
    total_doctors || ' total doctors (' || active_doctors || ' active)' as doctors_status,
    total_preferences || ' preference submissions across ' || months_with_preferences || ' months' as preferences_status,
    total_scheduled_shifts || ' scheduled shifts across ' || months_with_schedule || ' months' as schedule_status,
    CASE 
        WHEN total_doctors >= 25 AND active_doctors >= 20 THEN '✅ Doctor data looks good'
        ELSE '⚠️ Check doctor data'
    END as doctor_health,
    CASE 
        WHEN total_preferences > 0 THEN '✅ Preferences system ready'
        ELSE 'ℹ️ No preferences yet (normal for new setup)'
    END as preferences_health,
    '🚀 Database ready for MICU Scheduler app!' as final_status
FROM summary;

-- =============================================================================
-- TROUBLESHOOTING QUERIES
-- =============================================================================

/*
-- If you see any issues, run these additional diagnostic queries:

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE tablename IN ('doctors', 'preferences', 'schedule');

-- Check for locks
SELECT 
    pid,
    usename,
    application_name,
    state,
    query
FROM pg_stat_activity
WHERE datname = current_database()
    AND state != 'idle';

-- Check recent activity
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    last_vacuum,
    last_analyze
FROM pg_stat_user_tables
WHERE tablename IN ('doctors', 'preferences', 'schedule');
*/

-- =============================================================================
-- SUCCESS MESSAGE
-- =============================================================================

DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '🎉 Verification complete! If all queries above ran without errors,';
    RAISE NOTICE '   your Supabase database is correctly configured for the MICU Scheduler.';
    RAISE NOTICE '';
    RAISE NOTICE '📋 Next steps:';
    RAISE NOTICE '   1. Copy your DATABASE_URL from Supabase Settings → Database';
    RAISE NOTICE '   2. Add it to your Vercel environment variables';
    RAISE NOTICE '   3. Deploy your application';
    RAISE NOTICE '';
    RAISE NOTICE '🔧 Need test data? Run the supabase_seed.sql script';
    RAISE NOTICE '';
END $$;