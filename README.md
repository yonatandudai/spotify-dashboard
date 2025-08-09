# Spotify Profile Demo

A full-stack application that displays your Spotify profile data using the Spotify Web API.

## Features

- 🔐 Spotify OAuth authentication
- 👤 Display user profile information
- 🎵 Show top tracks and artists
- 📱 Responsive design
- ⚡ Real-time data fetching

## Tech Stack

**Frontend:**
- React 18
- TypeScript
- Vite
- CSS3

**Backend:**
- Python 3.8+
- FastAPI
- Requests
- python-dotenv

## Setup Instructions

### 1. Spotify App Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click "Create app"
3. Fill in the details:
   - **App name**: Spotify Profile Demo
   - **App description**: A demo app to display Spotify profile data
   - **Redirect URI**: `http://localhost:8000/api/auth/callback`
   - **APIs used**: Web API
4. Save your app
5. Copy your **Client ID** and **Client Secret**

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
copy .env.example .env
# Edit .env file with your Spotify credentials
```

**Edit `.env` file:**
```env
SPOTIFY_CLIENT_ID=your_client_id_from_spotify_dashboard
SPOTIFY_CLIENT_SECRET=your_client_secret_from_spotify_dashboard
SPOTIFY_REDIRECT_URI=http://localhost:8000/api/auth/callback
SESSION_SECRET_KEY=your_random_secret_key_here
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd spotify-profile-demo

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Running the Application

1. **Start the backend server:**
   ```bash
   cd backend
   python main.py
   ```
   Backend will run on `http://localhost:8000`

2. **Start the frontend development server:**
   ```bash
   cd spotify-profile-demo
   npm run dev
   ```
   Frontend will run on `http://localhost:3000`

3. **Open your browser** and go to `http://localhost:3000`

## Usage

1. Click "Login with Spotify" button
2. Authorize the app on Spotify
3. View your profile data and top tracks
4. Use the "Refresh Data" button to update your information

## API Endpoints

- `GET /api/auth/login` - Initiate Spotify OAuth
- `GET /api/auth/callback` - Handle OAuth callback
- `POST /api/auth/logout` - Logout user
- `GET /api/user/profile` - Get user profile
- `GET /api/user/top-tracks` - Get user's top tracks
- `GET /api/user/top-artists` - Get user's top artists
- `GET /api/user/playlists` - Get user's playlists

## Environment Variables

### Backend (.env)
- `SPOTIFY_CLIENT_ID` - Your Spotify app client ID
- `SPOTIFY_CLIENT_SECRET` - Your Spotify app client secret
- `SPOTIFY_REDIRECT_URI` - OAuth redirect URI
- `SESSION_SECRET_KEY` - Secret key for session management

## Security Notes

- This demo uses in-memory session storage. For production, use Redis or a database.
- The session cookie is set with `secure=False` for development. Set to `True` in production with HTTPS.
- Generate a strong random secret key for production use.

## Development

### Frontend Development
- Uses Vite for fast development and building
- TypeScript for type safety
- Modular CSS for styling

### Backend Development
- FastAPI provides automatic API documentation at `http://localhost:8000/docs`
- CORS enabled for frontend communication
- RESTful API design

## Troubleshooting

1. **"Authorization code not provided" error**: Check your Spotify app redirect URI
2. **CORS errors**: Ensure backend is running on port 8000 and frontend on port 3000
3. **"Not authenticated" errors**: Clear cookies and try logging in again
4. **Token expired errors**: The app should handle this automatically, but you may need to re-login

## License

This project is for educational purposes. Make sure to comply with Spotify's Developer Terms of Service.
