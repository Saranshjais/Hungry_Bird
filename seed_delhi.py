# seed_delhi.py

from app import create_app, db
from app.models import City, Vendor

app = create_app()

with app.app_context():
    # Ensure Delhi city exists
    delhi = City.query.filter_by(slug="delhi").first()
    if not delhi:
        delhi = City(
            name="Delhi",
            slug="delhi",
            state="Delhi",
            country="India",
            lat=28.7041,
            lng=77.1025,
        )
        db.session.add(delhi)
        db.session.commit()
        print("Added city: Delhi, id =", delhi.id)
    else:
        print("Delhi already exists, id =", delhi.id)

    # Define some Delhi vendors
    vendors_delhi = [
        ("Paranthe Wali Gali", "Stuffed Parathas", "Chandni Chowk", 28.6562, 77.2300),
        ("Karim's Jama Masjid", "Mughlai, Kebabs", "Jama Masjid", 28.6509, 77.2335),
        ("Kuremal Mohan Lal Kulfi", "Stuffed Kulfi", "Chawri Bazar", 28.6500, 77.2305),
        ("Bittoo Tikki Wala", "Aloo Tikki, Chaat", "Karol Bagh", 28.6516, 77.1893),
        ("Dolma Aunty Momos", "Momos", "Lajpat Nagar", 28.5694, 77.2433),
        ("Roshan Di Kulfi", "Kulfi Falooda, Chole Bhature", "Karol Bagh", 28.6510, 77.1904),
        ("Al-Bake", "Shawarma, Rolls", "New Friends Colony", 28.5613, 77.2708),
        ("Atul Chaat Corner", "Chaat, Chhole Bhature", "Rajouri Garden", 28.6424, 77.1167),
    ]

    added_count = 0

    for name, cuisine, area, lat, lng in vendors_delhi:
        existing = Vendor.query.filter_by(name=name, city_id=delhi.id).first()
        if existing:
            print("Skipping (exists):", name)
            continue

        v = Vendor(
            city_id=delhi.id,
            name=name,
            cuisine_type=cuisine,
            is_hidden_gem=True,
            is_famous=True,
            avg_rating=None,
            price_level="₹100–₹250",
            address_text=area,
            area=area,
            lat=lat,
            lng=lng,
            source="admin",
            verified_status="verified",
        )
        db.session.add(v)
        added_count += 1
        print("Added Delhi vendor:", name)

    db.session.commit()

    print("\nDone seeding Delhi!")
    print("Total Delhi vendors now:",
          Vendor.query.filter_by(city_id=delhi.id).count())
