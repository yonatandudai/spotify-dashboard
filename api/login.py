# Vercel Function: Login
from http.server import BaseHTTPRequestHandler
import urllib.parse
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get Spotify credentials
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        
        if not client_id:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"error": "SPOTIFY_CLIENT_ID not configured"}')
            return
        
        # Spotify OAuth scopes
        scopes = [
            "user-read-private",
            "user-read-email", 
            "user-top-read"
        ]
        
        # Build auth URL
        auth_params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": " ".join(scopes)
        }
        
        auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(auth_params)}"
        
        # Redirect to Spotify
        self.send_response(302)
        self.send_header('Location', auth_url)
        self.end_headers()
        return
