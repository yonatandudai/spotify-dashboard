# Vercel Function: API Root
from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Simple API info
        response = {
            "message": "Spotify API is working!",
            "path": self.path,
            "method": self.command,
            "env_check": {
                "client_id": bool(os.getenv('SPOTIFY_CLIENT_ID')),
                "client_secret": bool(os.getenv('SPOTIFY_CLIENT_SECRET')),
                "redirect_uri": os.getenv('SPOTIFY_REDIRECT_URI', 'not_set')
            }
        }
        
        self.wfile.write(json.dumps(response).encode())
        return
