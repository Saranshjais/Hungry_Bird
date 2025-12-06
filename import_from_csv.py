import csv
from app import db, create_app
from app.models import City, Vendor

app = create_app()

CSV_PATH = "google_places_vendors.csv"  # CSV must be in root folder


def slugify(value: str) -> str:
    return (
        value.lower()
        .replace("&", "and")
        .replace("'", "")
        .replace("/", "-")
        .replace(" ", "-")
    )


with app.app_context():
    print("🔄 Deleting all existing vendors...")
    Vendor.query.delete()
    db.session.commit()
    print("✅ Existing vendors cleared.\n")

    # Cache existing cities
    cities_cache = {c.name.strip().lower(): c for c in City.query.all()}
    
    def get_or_create_city(city_name: str):
        key = city_name.lower()
        city = cities_cache.get(key)
        if city:
            return city

        slug = slugify(city_name)
        city = City(name=city_name, slug=slug)
        db.session.add(city)
        db.session.flush()
        cities_cache[key] = city
        print(f"🏙 Added new city: {city_name}")
        return city

    count = 0

    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):

            name = row.get("name", "").strip()
            city_name = row.get("city", "").strip()

            if not name or not city_name:
                continue

            # Parse coordinates
            try:
                lat = float(row.get("latitude"))
                lng = float(row.get("longitude"))
            except:
                continue

            city = get_or_create_city(city_name)

            rating = None
            rating_raw = row.get("rating")
            if rating_raw not in (None, "", "NaN", "nan"):
                try:
                    rating = float(rating_raw)
                except:
                    rating = None

            # Directly take image from CSV
            image_url = row.get("image") or None

            vendor = Vendor(
                city_id=city.id,
                name=name,
                cuisine_type=row.get("cuisine") or "Street Food",
                address_text=row.get("formatted_address") or None,
                avg_rating=rating,
                lat=lat,
                lng=lng,
                image_url=image_url,
                source="google_csv",
                verified_status="verified",
                is_hidden_gem=False,
                is_famous=True
            )

            db.session.add(vendor)
            count += 1

    db.session.commit()
    print(f"\n🎉 Successfully imported {count} Google Vendors!")
