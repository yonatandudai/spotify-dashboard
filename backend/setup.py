#!/usr/bin/env python3
"""
Setup script for Spotify Profile Demo backend
"""
import os
import secrets
import subprocess
import sys

def create_env_file():
    """Create .env file with placeholder values"""
    env_content = f"""# Spotify API credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8000/api/auth/callback

# Session secret key (generated)
SESSION_SECRET_KEY={secrets.token_urlsafe(32)}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with generated secret key")
    print("⚠️  Remember to update SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET")

def install_dependencies():
    """Install Python dependencies"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Installed Python dependencies")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    return True

def main():
    print("🎵 Setting up Spotify Profile Demo Backend...\n")
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping creation.")
    else:
        create_env_file()
    
    # Install dependencies
    if install_dependencies():
        print("\n✅ Backend setup complete!")
        print("\n📋 Next steps:")
        print("1. Edit the .env file with your Spotify app credentials")
        print("2. Run: python main.py")
        print("3. Backend will be available at http://localhost:8000")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
