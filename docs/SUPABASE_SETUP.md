# 🗄️ Supabase Database Setup for MICU Scheduler

## Step-by-Step Supabase Setup

### 1. Create Supabase Project

1. **Go to [Supabase](https://supabase.com/dashboard)**
2. **Click "New Project"**
3. **Fill in project details:**
   - **Name**: `micu-scheduler` (or your preferred name)
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Select closest to your users (e.g., `us-east-1` for North America)
4. **Click "Create new project"**
5. **Wait 2-3 minutes for setup to complete**

### 2. Get Database Connection Details

1. **In your Supabase dashboard, go to Settings → Database**
2. **Copy the Connection String (URI format):**
   ```
   postgresql://postgres.xxxxxxxxxxxx:[YOUR-PASSWORD]@db.xxxxxxxxxxxx.supabase.co:5432/postgres
   ```
3. **Save this URL - you'll need it for Vercel environment variables**

### 3. Run Database Schema

1. **In Supabase dashboard, go to SQL Editor**
2. **Click "New Query"**
3. **Copy and paste the complete schema from `database/supabase_schema.sql`**
4. **Click "Run" (or press Ctrl/Cmd + Enter)**
5. **Verify success - you should see "Success. No rows returned"**

### 4. Verify Tables Created

1. **Go to Table Editor in Supabase dashboard**
2. **You should see 3 tables:**
   - `doctors` (25 Rush MICU doctors)
   - `preferences` (empty, ready for doctor submissions)
   - `schedule` (empty, ready for generated schedules)

### 5. Test Database Connection

Run this query in SQL Editor to verify everything works:

```sql
-- Test basic functionality
SELECT 
    d.name,
    d.initials,
    d.active,
    COUNT(p.id) as preferences_submitted,
    COUNT(s.id) as shifts_scheduled
FROM doctors d
LEFT JOIN preferences p ON d.id = p.doctor_id
LEFT JOIN schedule s ON d.id = s.doctor_id
WHERE d.active = true
GROUP BY d.id, d.name, d.initials, d.active
ORDER BY d.name;
```

**Expected result:** List of 25 active doctors with 0 preferences and 0 shifts (initially).

## 🔧 Configuration for Vercel

After setting up Supabase, add these environment variables in your **Vercel dashboard**:

### Environment Variables

```bash
# Database Connection (from Supabase Settings → Database)
DATABASE_URL=postgresql://postgres.xxxxxxxxxxxx:[YOUR-PASSWORD]@db.xxxxxxxxxxxx.supabase.co:5432/postgres

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false

# Python Runtime
PYTHONPATH=/var/task
```

## 🚀 Ready to Deploy!

Once you've:
1. ✅ Created Supabase project
2. ✅ Run the schema script
3. ✅ Verified tables exist
4. ✅ Added environment variables to Vercel

Your MICU Scheduler is ready to deploy on Vercel!

## 🔍 Troubleshooting

### Common Issues

**"relation does not exist" errors:**
- Make sure you ran the complete schema script
- Check that all tables were created in Table Editor

**Connection timeouts:**
- Verify your DATABASE_URL is correct
- Check Supabase project is active (not paused)

**Permission errors:**
- Ensure you're using the correct database password
- Check that your connection string includes the password

**Want to start fresh?**
- Run the cleanup script from `database/supabase_cleanup.sql`
- Then re-run the schema script

## 📊 Optional: Add Test Data

For development/testing, you can add sample preferences:

```sql
-- Add some test preferences (run in Supabase SQL Editor)
INSERT INTO preferences (doctor_id, month, unavailable, preferred, desired_shifts) VALUES
(1, '2025-01', ARRAY['2025-01-15', '2025-01-16'], ARRAY['2025-01-01', '2025-01-02'], 7),
(2, '2025-01', ARRAY['2025-01-10', '2025-01-11'], ARRAY['2025-01-20', '2025-01-21'], 8),
(3, '2025-01', ARRAY['2025-01-25'], ARRAY['2025-01-05', '2025-01-06', '2025-01-07'], 6);
```

This allows you to test the scheduling algorithm immediately.

---

**Need help?** Check the full deployment guide in `docs/DEPLOYMENT.md` or the troubleshooting section.