import os
import secrets
import urllib.parse
import requests
from typing import Optional, Dict, Any

try:
    from fastapi import FastAPI, HTTPException, Request, Response
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import RedirectResponse
    from mangum import Mangum
except ImportError as e:
    print(f"❌ Import error: {e}")
    raise

# FastAPI app
app = FastAPI(title="Spotify Profile API")

# Configure CORS - Production ready
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "http://localhost:3001", 
        "http://localhost:3002",
        "https://*.vercel.app",   # Vercel deployment
        "https://*.netlify.app",  # Netlify deployment
        "https://*.railway.app",  # Railway deployment
        "https://*.render.com",   # Render deployment
        "https://*.herokuapp.com", # Heroku deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Spotify API configuration
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "fallback-secret-key")

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

# In-memory session storage (use Redis or database in production)
user_sessions: Dict[str, Dict[str, Any]] = {}

def generate_session_id() -> str:
    """Generate a secure session ID"""
    return secrets.token_urlsafe(32)

def get_user_session(request: Request) -> Optional[Dict[str, Any]]:
    """Get user session from cookies"""
    session_id = request.cookies.get("session_id")
    print(f"DEBUG: Looking for session_id: {session_id}")
    print(f"DEBUG: Available sessions: {list(user_sessions.keys())}")
    if session_id and session_id in user_sessions:
        print(f"DEBUG: Session found!")
        return user_sessions[session_id]
    print(f"DEBUG: No session found")
    return None

def set_user_session(response: Response, session_data: Dict[str, Any]) -> str:
    """Set user session and return session ID"""
    session_id = generate_session_id()
    user_sessions[session_id] = session_data
    # Set cookie with proper settings for production
    response.set_cookie(
        "session_id", 
        session_id, 
        httponly=True, 
        secure=True,  # True for production HTTPS
        samesite="lax",  # Allow cross-site requests for OAuth
        path="/",
        max_age=3600  # 1 hour expiration
    )
    print(f"DEBUG: Setting cookie with session_id: {session_id}")
    return session_id

def make_spotify_request(endpoint: str, access_token: str) -> Dict[str, Any]:
    """Make authenticated request to Spotify API"""
    headers = {"Authorization": f"Bearer {access_token}"}
    full_url = f"{SPOTIFY_API_BASE_URL}{endpoint}"
    print(f"🔗 DEBUG: Full Spotify URL: {full_url}")
    
    response = requests.get(full_url, headers=headers)
    
    print(f"📊 DEBUG: Spotify API response status: {response.status_code}")
    
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Spotify token expired")
    elif response.status_code != 200:
        print(f"❌ DEBUG: Spotify API error response: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Spotify API error")
    
    response_data = response.json()
    print(f"✅ DEBUG: Got {len(response_data.get('items', []))} items from Spotify")
    return response_data

@app.get("/")
async def root():
    return {"message": "Spotify Profile API is running!", "timestamp": "2025-08-09", "version": "1.0"}

@app.get("/api")
async def api_root():
    return {"message": "API endpoint working!", "routes": ["auth/login", "auth/callback", "user/profile", "user/top-tracks", "user/top-artists"]}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "env_vars": {
            "client_id_set": bool(SPOTIFY_CLIENT_ID),
            "client_secret_set": bool(SPOTIFY_CLIENT_SECRET),
            "redirect_uri": SPOTIFY_REDIRECT_URI
        }
    }

@app.get("/api/config/check")
async def check_config():
    """Check if Spotify credentials are configured"""
    client_id_configured = bool(SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_ID != "your_spotify_client_id_here")
    client_secret_configured = bool(SPOTIFY_CLIENT_SECRET and SPOTIFY_CLIENT_SECRET != "your_spotify_client_secret_here")
    
    return {
        "client_id_configured": client_id_configured,
        "client_secret_configured": client_secret_configured,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "ready": client_id_configured and client_secret_configured
    }

@app.get("/api/auth/login")
async def login():
    """Initiate Spotify OAuth login"""
    if not SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_ID == "your_spotify_client_id_here":
        raise HTTPException(
            status_code=500, 
            detail="Spotify Client ID not configured. Please update your environment variables with real Spotify credentials."
        )
    
    if not SPOTIFY_CLIENT_SECRET or SPOTIFY_CLIENT_SECRET == "your_spotify_client_secret_here":
        raise HTTPException(
            status_code=500, 
            detail="Spotify Client Secret not configured. Please update your environment variables with real Spotify credentials."
        )
    
    # Spotify OAuth scopes
    scopes = [
        "user-read-private",
        "user-read-email",
        "user-top-read",
        "user-read-recently-played",
        "playlist-read-private"
    ]
    
    # Generate state parameter for security
    state = secrets.token_urlsafe(16)
    
    auth_params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": " ".join(scopes),
        "state": state
    }
    
    auth_url = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(auth_params)}"
    return RedirectResponse(url=auth_url)

@app.get("/api/auth/callback")
async def callback(request: Request, response: Response, code: str = None, state: str = None, error: str = None):
    """Handle Spotify OAuth callback"""
    print(f"DEBUG: Callback called with code={code}, state={state}, error={error}")
    
    if error:
        raise HTTPException(status_code=400, detail=f"Spotify authorization error: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")
    
    # Exchange authorization code for access token
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    
    print(f"DEBUG: Making token request to Spotify...")
    token_response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)
    print(f"DEBUG: Token response status: {token_response.status_code}")
    
    if token_response.status_code != 200:
        error_detail = f"Failed to exchange authorization code. Status: {token_response.status_code}"
        try:
            error_info = token_response.json()
            print(f"DEBUG: Token error response: {error_info}")
            if "error_description" in error_info:
                error_detail += f", Error: {error_info['error_description']}"
            elif "error" in error_info:
                error_detail += f", Error: {error_info['error']}"
        except Exception as e:
            print(f"DEBUG: Could not parse error response: {e}")
            error_detail += f", Response: {token_response.text}"
        
        raise HTTPException(status_code=400, detail=error_detail)
    
    token_info = token_response.json()
    print(f"DEBUG: Token exchange successful, got access_token")
    
    # Store tokens in session
    session_data = {
        "access_token": token_info["access_token"],
        "refresh_token": token_info.get("refresh_token"),
        "expires_in": token_info["expires_in"]
    }
    
    session_id = set_user_session(response, session_data)
    print(f"DEBUG: Session created with ID: {session_id}")
    
    # Redirect back to frontend
    frontend_url = os.getenv("FRONTEND_URL", request.url.scheme + "://" + request.url.netloc)
    redirect_url = f"{frontend_url}?auth_complete=true&session_id={session_id}"
    print(f"DEBUG: Redirecting to: {redirect_url}")
    return RedirectResponse(url=redirect_url)

@app.get("/api/user/profile")
async def get_user_profile(request: Request):
    """Get current user's Spotify profile"""
    session = get_user_session(request)
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        profile_data = make_spotify_request("/me", session["access_token"])
        return profile_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching profile: {str(e)}")

@app.get("/api/user/top-tracks")
async def get_top_tracks(request: Request, limit: int = 20, time_range: str = "medium_term"):
    """Get user's top tracks"""
    session = get_user_session(request)
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Validate parameters
    if limit > 50:
        limit = 50
    if time_range not in ["short_term", "medium_term", "long_term"]:
        time_range = "medium_term"
    
    try:
        endpoint = f"/me/top/tracks?limit={limit}&time_range={time_range}"
        tracks_data = make_spotify_request(endpoint, session["access_token"])
        return tracks_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching top tracks: {str(e)}")

@app.get("/api/user/top-artists")
async def get_top_artists(request: Request, limit: int = 20, time_range: str = "medium_term"):
    """Get user's top artists"""
    print(f"🔍 DEBUG: Received request with limit={limit}, time_range='{time_range}'")
    
    session = get_user_session(request)
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Validate parameters
    if limit > 50:
        limit = 50
    if time_range not in ["short_term", "medium_term", "long_term"]:
        print(f"⚠️  DEBUG: Invalid time_range '{time_range}', defaulting to medium_term")
        time_range = "medium_term"
    
    print(f"🎤 DEBUG: Fetching top artists with limit={limit}, time_range={time_range}")
    
    try:
        endpoint = f"/me/top/artists?limit={limit}&time_range={time_range}"
        print(f"🎤 DEBUG: Spotify endpoint: {endpoint}")
        artists_data = make_spotify_request(endpoint, session["access_token"])
        print(f"🎤 DEBUG: Got {len(artists_data.get('items', []))} artists")
        if artists_data.get('items'):
            print(f"🎤 DEBUG: First 3 artists: {[a['name'] for a in artists_data['items'][:3]]}")
        return artists_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching top artists: {str(e)}")

@app.post("/api/auth/logout")
async def logout(response: Response, request: Request):
    """Logout user"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in user_sessions:
        del user_sessions[session_id]
    
    response.delete_cookie("session_id")
    return {"message": "Logged out successfully"}

# Add some debugging for Vercel
print("🚀 API module loaded successfully")
print(f"🔍 Environment check:")
print(f"  - SPOTIFY_CLIENT_ID: {os.getenv('SPOTIFY_CLIENT_ID', 'NOT_SET')}")
print(f"  - SPOTIFY_CLIENT_SECRET: {'SET' if os.getenv('SPOTIFY_CLIENT_SECRET') else 'NOT_SET'}")
print(f"  - SPOTIFY_REDIRECT_URI: {os.getenv('SPOTIFY_REDIRECT_URI', 'NOT_SET')}")

# Create the handler for Vercel
from mangum import Mangum

# Create the Mangum handler
handler = Mangum(app)
