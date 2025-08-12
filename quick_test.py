import requests

def test_vercel_endpoints():
    base_url = "https://spotify-dashboard-j9imvto25-yonatan-dudais-projects.vercel.app"
    
    endpoints = [
        "/api/status",
        "/api/login", 
        "/api/test"
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\n🧪 Testing: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"✅ Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    print(f"📄 Response: {response.json()}")
                except:
                    print(f"📄 Response: {response.text[:200]}")
            else:
                print(f"❌ Error: {response.text[:200]}")
        except Exception as e:
            print(f"💥 Exception: {e}")

if __name__ == "__main__":
    test_vercel_endpoints()
