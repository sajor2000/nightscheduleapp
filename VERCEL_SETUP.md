# ⚡ Quick Vercel Deployment Setup

## 🚀 Deploy to Vercel in 5 Minutes

### 1. Import to Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import from GitHub: `https://github.com/sajor2000/nightscheduleapp`

### 2. Add Environment Variables
In Vercel dashboard → Settings → Environment Variables, add:

```bash
# Database Connection (from your .env file)
DATABASE_URL
postgres://postgres.ivbhvsaeumpaprjtxhgw:yPGJLR8tI1iS225e@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require

# Flask Config
FLASK_ENV
production

FLASK_DEBUG
false

# Python Runtime
PYTHONPATH
/var/task

# Frontend Environment
REACT_APP_ENVIRONMENT
production
```

### 3. Deploy!
Click "Deploy" - Vercel will:
- ✅ Build React frontend
- ✅ Deploy serverless functions
- ✅ Connect to Supabase
- ✅ Provide live URL

### 4. Test Your Deployment
Visit your Vercel URL:
- **Health Check**: `https://your-app.vercel.app/api/health`
- **Main App**: `https://your-app.vercel.app`

## 🔧 Troubleshooting

**Build fails?**
- Check environment variables are set correctly
- Verify DATABASE_URL format

**Database errors?**
- Run the schema script in Supabase SQL Editor first
- Check database URL includes `?sslmode=require`

**API not working?**
- Test health endpoint first: `/api/health`
- Check Vercel function logs

## ✅ Success!
Your MICU Scheduler should now be live on Vercel! 🎉