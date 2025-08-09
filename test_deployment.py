#!/usr/bin/env python3
"""
Test script for Vercel deployment
"""
import requests
import json

BASE_URL = "https://spotify-dashboard-seven.vercel.app"

def test_endpoint(endpoint, description):
    """Test a specific endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n🧪 Testing {description}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            except:
                print(f"Response: {response.text}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    print("-" * 50)

if __name__ == "__main__":
    print("🚀 Testing Vercel Deployment")
    print("=" * 50)
    
    # Test endpoints
    test_endpoint("/", "Frontend")
    test_endpoint("/api", "API Root")
    test_endpoint("/api/health", "Health Check")
    test_endpoint("/api/config/check", "Config Check")
    
    print("\n✅ Testing complete!")
    print("\nIf all endpoints return 200 OK, try the login flow:")
    print(f"{BASE_URL}/api/auth/login")
