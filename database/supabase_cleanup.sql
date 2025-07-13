-- 🧹 MICU Scheduler - Database Cleanup Script
-- Use this to reset/clean your Supabase database if needed

-- =============================================================================
-- COMPLETE DATABASE RESET
-- WARNING: This will delete ALL data! Use with caution.
-- =============================================================================

-- Remove all triggers first
DROP TRIGGER IF EXISTS schedule_update_modified_at ON schedule;

-- Remove functions
DROP FUNCTION IF EXISTS update_modified_at();
DROP FUNCTION IF EXISTS validate_date_format(TEXT[]);

-- Remove all tables (CASCADE will handle foreign keys)
DROP TABLE IF EXISTS schedule CASCADE;
DROP TABLE IF EXISTS preferences CASCADE;
DROP TABLE IF EXISTS doctors CASCADE;

-- Remove indexes (they should be dropped with tables, but just in case)
DROP INDEX IF EXISTS idx_doctors_active;
DROP INDEX IF EXISTS idx_doctors_initials;
DROP INDEX IF EXISTS idx_preferences_month;
DROP INDEX IF EXISTS idx_preferences_doctor_month;
DROP INDEX IF EXISTS idx_schedule_month;
DROP INDEX IF EXISTS idx_schedule_date;
DROP INDEX IF EXISTS idx_schedule_doctor_month;

-- Success message
DO $$
BEGIN
    RAISE NOTICE '🧹 Database cleanup completed!';
    RAISE NOTICE '📋 All tables, functions, and triggers have been removed.';
    RAISE NOTICE '🔄 You can now re-run supabase_schema.sql for a fresh setup.';
END $$;