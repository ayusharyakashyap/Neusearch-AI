# 🚀 Deployment Guide - Neusearch Product Assistant

> **Zero-Config Deployment** - No API keys required! The app runs in fallback mode with demo data.

## ✅ Prerequisites Complete

- ✅ Code pushed to GitHub: `https://github.com/ayusharyakashyap/Neusearch-AI`
- ✅ All deployment configs ready
- ✅ Fallback mode enabled (works without OpenAI API)

---

## 📋 3-Step Deployment Checklist

### **Step 1: Deploy Backend to Render** ⚙️

1. **Go to [Render Dashboard](https://dashboard.render.com/)**
   - Sign in (or create free account)

2. **Click "New +" → "Blueprint"**

3. **Connect Repository**
   - Select your GitHub account
   - Choose repository: `ayusharyakashyap/Neusearch-AI`
   - Render will auto-detect `render.yaml`

4. **Review Resources**
   - Render will propose:
     - ✅ PostgreSQL Database (free tier)
     - ✅ Web Service (backend, free tier)
   - Click **"Apply"**

5. **Wait for Deployment** (~3-5 minutes)
   - Monitor build logs in Render dashboard
   - Once complete, copy your backend URL:
     ```
     https://neusearch-backend-XXXX.onrender.com
     ```

6. **Test Backend**
   ```bash
   curl https://your-backend-url.onrender.com/api/health
   # Expected: {"status":"ok"}
   ```

---

### **Step 2: Deploy Frontend to Vercel** 🎨

1. **Go to [Vercel Dashboard](https://vercel.com/new)**
   - Sign in with GitHub

2. **Import Project**
   - Click "Add New Project"
   - Select repository: `ayusharyakashyap/Neusearch-AI`

3. **Configure Project**
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend` ⚠️ (Important!)
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Add Environment Variable**
   - Click "Environment Variables"
   - Add:
     ```
     Name: REACT_APP_API_URL
     Value: https://your-backend-url.onrender.com
     ```
     (Use the URL from Step 1)

5. **Click "Deploy"**
   - Wait ~2 minutes for build
   - Once complete, get your frontend URL:
     ```
     https://neusearch-ai.vercel.app
     ```

---

### **Step 3: Test Deployment** 🧪

1. **Open Frontend**
   - Visit: `https://your-app.vercel.app`
   - Should see product grid with 6 demo products

2. **Test API Connection**
   ```bash
   # From browser console or terminal:
   curl https://your-backend-url.onrender.com/api/products
   # Should return JSON array of 6 products
   ```

3. **Test Chat Interface**
   - Navigate to "Chat Assistant"
   - Type: "I need furniture for my bedroom"
   - Should see AI recommendations (fallback mode)

4. **Verify All Pages**
   - ✅ Home page loads products
   - ✅ Product detail pages work
   - ✅ Chat interface responds
   - ✅ Navigation between pages works

---

## 🎉 You're Done!

Your app is now live at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.onrender.com`
- **API Docs**: `https://your-backend.onrender.com/docs`

---

## 🔧 Optional: Enable OpenAI

The app works perfectly in fallback mode, but if you want LLM-powered recommendations:

1. **Get OpenAI API Key**
   - Sign up at [platform.openai.com](https://platform.openai.com)
   - Create API key

2. **Add to Render**
   - Go to Render dashboard → your backend service
   - Environment → Add variable:
     ```
     OPENAI_API_KEY=sk-...your-key...
     ```
   - Service will auto-redeploy

3. **Test LLM Mode**
   - Ask abstract questions in chat
   - Should get more intelligent, contextual responses

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: Health check fails
```bash
# Check logs in Render dashboard
# Common fix: Wait 2-3 minutes for cold start
```

**Problem**: Database connection errors
```bash
# Render auto-injects DATABASE_URL
# Check Environment tab → DATABASE_URL is present
```

### Frontend Issues

**Problem**: "Failed to fetch" errors
```bash
# Check REACT_APP_API_URL in Vercel
# Settings → Environment Variables
# Must NOT include /api suffix (we add it in code)
```

**Problem**: CORS errors
```bash
# Backend already configured with CORS: allow all origins
# Check browser console for exact error
# Verify backend URL is correct (no trailing slash)
```

### Free Tier Limits

**Render Free Tier**:
- 750 hours/month (enough for 24/7 uptime)
- Spins down after 15 min inactivity
- First request after spin-down takes ~30 seconds

**Vercel Free Tier**:
- 100 GB bandwidth/month
- Unlimited deployments
- No sleep/spin-down

---

## 📊 What's Deployed

### Backend Features ✅
- FastAPI REST API
- PostgreSQL database (auto-seeded with 6 products)
- Vector search (ChromaDB)
- Fallback recommendations (keyword matching)
- Optional OpenAI integration
- Auto-scaling on Render

### Frontend Features ✅
- React SPA
- Product browsing
- AI chat assistant
- Responsive design
- Deployed on Vercel CDN

### Infrastructure ✅
- Database: Managed PostgreSQL (Render)
- Backend: Container deployment (Render)
- Frontend: Static site (Vercel)
- CI/CD: GitHub Actions
- Monitoring: Render logs, Vercel analytics

---

## 📹 Recording Your Loom Video

Now that everything's deployed, record your demo:

### What to Show (2-3 minutes):

1. **Live Site Overview** (30s)
   - Open deployed URL
   - Show homepage with products
   - Navigate to product detail

2. **Chat Functionality** (60s)
   - Go to Chat Assistant
   - Ask: "I need furniture for my bedroom"
   - Ask: "Small apartment storage"
   - Show product recommendations

3. **Architecture Quick Tour** (30s)
   - Show GitHub repo
   - Point out key files: `render.yaml`, `docker-compose.yml`
   - Mention RAG pipeline (ChromaDB + fallback LLM)

4. **Deployment** (30s)
   - Show Render dashboard (backend running)
   - Show Vercel dashboard (frontend deployed)
   - Emphasize zero-config deployment

### Loom Recording Tips:
- Visit [loom.com](https://loom.com)
- Use "Screen & Camera" mode
- Keep it casual and conversational
- Show real interactions (not just slides)
- Highlight the fallback mode (no API keys needed)

---

## 🎯 Submission Checklist

Final submission should include:

- [x] **GitHub Repository**: `https://github.com/ayusharyakashyap/Neusearch-AI`
- [ ] **Live Backend URL**: `https://neusearch-backend-XXXX.onrender.com`
- [ ] **Live Frontend URL**: `https://neusearch-ai.vercel.app`
- [ ] **Loom Video**: `https://loom.com/share/...`

Submit via: **[Google Form Link from Assignment]**

---

## 💡 Pro Tips

1. **Keep Render Service Alive**
   - Add to UptimeRobot for health check pings
   - Prevents cold starts

2. **Monitor Costs**
   - Render/Vercel free tiers are generous
   - Should cost $0 for demo purposes

3. **Update Backend URL**
   - If you redeploy backend, update `REACT_APP_API_URL` in Vercel
   - Vercel will auto-redeploy frontend

4. **Local Development**
   - Use `docker-compose up` for full stack locally
   - Copy `.env.example` to `.env` first

---

**Questions?** Check logs in Render/Vercel dashboards or GitHub Actions runs.

**Good luck! 🚀**
