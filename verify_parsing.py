import re
import requests

def parse_url(google_maps_url):
    lat, lng = None, None
    try:
        if google_maps_url:
            # 1. Resolve short URLs
            if "goo.gl" in google_maps_url or "maps.app.goo.gl" in google_maps_url:
                try:
                    resp = requests.head(google_maps_url, allow_redirects=True, timeout=5)
                    google_maps_url = resp.url
                    print(f"Resolved to: {google_maps_url}")
                except Exception as e:
                    print(f"Short URL resolution failed: {e}")

            # 2. Case 1: @lat,lng
            match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', google_maps_url)
            if match:
                lat = float(match.group(1))
                lng = float(match.group(2))

            # 3. Case 2: !3dLAT!4dLNG
            if lat is None:
                match = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', google_maps_url)
                if match:
                    lat = float(match.group(1))
                    lng = float(match.group(2))

            # 4. Case 3: q= or query= lat,lng
            if lat is None:
                param = None
                if "query=" in google_maps_url:
                    param = "query="
                elif "q=" in google_maps_url:
                    param = "q="
                
                if param:
                    coords = google_maps_url.split(param)[-1].split("&")[0]
                    parts = coords.split(",")
                    if len(parts) == 2:
                        try:
                            lat = float(parts[0])
                            lng = float(parts[1])
                        except:
                            pass

            # 5. Validation
            if lat is not None and (lat < -90 or lat > 90): lat = None
            if lng is not None and (lng < -180 or lng > 180): lng = None
            
    except Exception as e:
        print("Map parsing failed:", e)
    
    return lat, lng

# Test cases
test_urls = [
    "https://www.google.com/maps/@26.9124,75.7873,15z",
    "https://www.google.com/maps/place/Jaipur/@26.9124,75.7873,12z/data=!3m1!4b1!4m6!3m5!1s0x396db61234b031e7:0x70af3013d5d13ee9!8m2!3d26.9124336!4d75.7872709!16zL20vMGN2eW0",
    "https://maps.app.goo.gl/3fX8W9Z8Z8Z8Z8Z8Z", # This will fail to resolve but test the logic
    "https://www.google.com/maps/search/?api=1&query=26.9124,75.7873"
]

for url in test_urls:
    l, n = parse_url(url)
    print(f"URL: {url}\nResult: {l}, {n}\n")
