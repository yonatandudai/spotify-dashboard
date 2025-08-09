"""
Spotify Credentials Setup Helper
Run this script to easily update your .env file with Spotify credentials
"""
import os
import re

def update_env_credentials():
    print("🎵 Spotify Credentials Setup")
    print("=" * 50)
    print()
    print("Before running this, make sure you have:")
    print("1. Created a Spotify app at: https://developer.spotify.com/dashboard")
    print("2. Set the redirect URI to: http://localhost:8000/api/auth/callback")
    print("3. Copied your Client ID and Client Secret")
    print()
    
    # Get credentials from user
    client_id = input("Enter your Spotify Client ID: ").strip()
    if not client_id:
        print("❌ Client ID cannot be empty!")
        return
    
    client_secret = input("Enter your Spotify Client Secret: ").strip()
    if not client_secret:
        print("❌ Client Secret cannot be empty!")
        return
    
    # Read current .env file
    env_path = ".env"
    if not os.path.exists(env_path):
        print("❌ .env file not found!")
        return
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Replace placeholders - using simple string replacement to avoid regex issues
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('SPOTIFY_CLIENT_ID='):
            lines[i] = f'SPOTIFY_CLIENT_ID={client_id}'
        elif line.startswith('SPOTIFY_CLIENT_SECRET='):
            lines[i] = f'SPOTIFY_CLIENT_SECRET={client_secret}'
    
    content = '\n'.join(lines)
    
    # Write back to file
    with open(env_path, 'w') as f:
        f.write(content)
    
    print()
    print("✅ Successfully updated .env file!")
    print("🔄 Please restart your backend server for changes to take effect.")
    print()
    print("Next steps:")
    print("1. Restart the backend: Ctrl+C then run the server again")
    print("2. Go to http://localhost:3000")
    print("3. Click 'Login with Spotify'")

if __name__ == "__main__":
    update_env_credentials()
