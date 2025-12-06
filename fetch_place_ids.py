import requests
from app import db, create_app
from app.models import Vendor

API_KEY = "AIzaSyCHcB96CTjIPTZsCrYXho9EWoHbBrk_B7I"

app = create_app()

with app.app_context():
    vendors = Vendor.query.all()
    print(f"Fetching place IDs for {len(vendors)} vendors...")

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    updated = 0

    for v in vendors:
        params = {
            "location": f"{v.lat},{v.lng}",
            "radius": 20,
            "key": API_KEY
        }

        res = requests.get(url, params=params).json()
        results = res.get("results", [])

        if not results:
            print(f"⚠️ No match found for: {v.name}")
            continue

        place = results[0]
        v.place_id = place.get("place_id")

        photos = place.get("photos")
        if photos:
            v.photo_reference = photos[0].get("photo_reference")

        updated += 1

    db.session.commit()
    print(f"\n🎉 Updated {updated} vendors with Place IDs")
