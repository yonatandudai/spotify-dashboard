# 🚀 Deployment Guide

Your Spotify Profile application is production-ready! Here are several deployment options:

## 🌐 Quick Deploy Options

### 1. **Railway (Recommended - Easiest Full-Stack)**

Railway is perfect for full-stack applications like this one.

1. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/yourusername/spotify-profile-app.git
   git push -u origin master
   ```

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub account
   - Select your repository
   - Railway will auto-detect and deploy both frontend and backend

3. **Set Environment Variables in Railway:**
   - `SPOTIFY_CLIENT_ID`: Your Spotify app client ID
   - `SPOTIFY_CLIENT_SECRET`: Your Spotify app client secret
   - `SPOTIFY_REDIRECT_URI`: `https://your-app.railway.app/api/auth/callback`
   - `SESSION_SECRET_KEY`: A strong random string

4. **Update Spotify App Settings:**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Add your Railway URL to redirect URIs: `https://your-app.railway.app/api/auth/callback`

### 2. **Render.com (Great Alternative)**

1. **Push to GitHub** (same as above)

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Connect GitHub and select your repo
   - Choose "Web Service"
   - Render will use the `render.yaml` configuration automatically

3. **Set Environment Variables** (same as Railway)

4. **Update Spotify App Settings** with your Render URL

### 3. **Vercel (Frontend) + Railway/Render (Backend)**

For separate deployment:

**Frontend (Vercel):**
1. Connect GitHub to Vercel
2. Deploy the `spotify-profile-demo` folder
3. Set build command: `npm run build`
4. Set output directory: `dist`

**Backend (Railway/Render):**
1. Deploy just the Python backend
2. Update CORS origins in `main.py` to include your Vercel URL

## 🔧 Production Checklist

### ✅ Security & Configuration
- [ ] Generate strong `SESSION_SECRET_KEY` (use: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- [ ] Set `ENVIRONMENT=production` in deployment
- [ ] Update Spotify app redirect URI to production URL
- [ ] Enable HTTPS on your deployment platform
- [ ] Review CORS settings in `main.py`

### ✅ Environment Variables Required
```env
SPOTIFY_CLIENT_ID=your_actual_client_id
SPOTIFY_CLIENT_SECRET=your_actual_client_secret
SPOTIFY_REDIRECT_URI=https://your-domain.com/api/auth/callback
SESSION_SECRET_KEY=your_very_secure_random_key_here
ENVIRONMENT=production
```

### ✅ Spotify App Configuration
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Select your app
3. Click "Edit Settings"
4. Add your production URL to "Redirect URIs":
   - `https://your-domain.com/api/auth/callback`
5. Save changes

## 📁 File Structure (Production Ready)
```
spotify-profile-app/
├── spotify-profile-demo/        # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.ts          # Production build config
├── main.py                     # FastAPI backend (production)
├── requirements.txt            # Python dependencies
├── package.json               # Root package.json for deployment
├── vercel.json                # Vercel configuration
├── railway.yml                # Railway configuration
├── render.yaml                # Render configuration
├── .env.example              # Environment template
├── .gitignore                # Git ignore file
└── README.md                 # Documentation
```

## 🎯 Post-Deployment Testing

1. **Test Authentication Flow:**
   - Visit your deployed app
   - Click "Login with Spotify"
   - Complete OAuth flow
   - Verify profile data loads

2. **Test API Endpoints:**
   - Profile: `https://your-domain.com/api/user/profile`
   - Tracks: `https://your-domain.com/api/user/top-tracks`
   - Artists: `https://your-domain.com/api/user/top-artists`

3. **Test Time Range Controls:**
   - Switch between short/medium/long term
   - Verify data updates correctly

## 🔍 Troubleshooting

### Common Issues:

**"Redirect URI mismatch"**
- Update Spotify app settings with exact production URL
- Ensure HTTPS is used in production

**"CORS errors"**
- Update `allow_origins` in `main.py` with your frontend domain
- Enable credentials in CORS configuration

**"Session not found"**
- Check cookie settings in production
- Verify `SESSION_SECRET_KEY` is set
- Consider using Redis for session storage in high-traffic production

**Environment variables not loading**
- Verify all required env vars are set in deployment platform
- Check `.env.example` for required variables

## 🚀 Ready to Deploy!

Your application includes:
- ✅ Professional UI with enhanced design
- ✅ Complete OAuth authentication flow
- ✅ Top tracks and artists with time controls
- ✅ Responsive design and error handling
- ✅ Production-ready configuration files
- ✅ Comprehensive documentation

Choose your deployment platform and follow the steps above. Your Spotify Profile app will be live in minutes!

---

**Quick Start**: We recommend **Railway** for the fastest deployment of your full-stack app.
