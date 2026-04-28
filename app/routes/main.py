from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from urllib.parse import urlparse, parse_qs
import re

from app import db, cache
from app.models import City, Vendor, VendorSubmission

# ✅ ML import
from app.ml_model import build_recommendation_model, get_recommendations

main_bp = Blueprint("main", __name__)


@cache.memoize(timeout=3600)
def get_cached_recommendations(city_id, vendor_list_tuple):
    # We use a tuple for vendor_list because cache keys must be hashable
    vendor_list = [dict(t) for t in vendor_list_tuple]
    if not vendor_list:
        return []
    try:
        df, similarity = build_recommendation_model(vendor_list)
        return get_recommendations(vendor_list[0]["name"], df, similarity)
    except Exception as e:
        print("ML error:", e)
        return []


# -------------------- HOME --------------------
@main_bp.route("/")
def index():
    cities = City.query.order_by(City.name).all()

    # ✅ Add food descriptions dynamically
    city_descriptions = {
        "jaipur": "Famous for Dal Baati Churma, rich spices, and traditional Rajasthani flavors.",
        "delhi": "Known for Chole Bhature, Golgappa, and diverse Mughlai cuisine.",
        "mumbai": "Popular for Vada Pav, Pav Bhaji, and vibrant street food culture.",
    }

    # Attach description to each city
    for city in cities:
        city.desc = city_descriptions.get(city.slug, "Explore local food and hidden gems.")

    return render_template("index.html", cities=cities)


# ✅ ADD HERE
def convert_price(p):
    if not p:
        return 100
    if "50" in str(p):
        return 50
    if "100" in str(p):
        return 100
    if "200" in str(p):
        return 200
    return 150
# -------------------- CITY PAGE --------------------
@main_bp.route("/city/<slug>")
def city_page(slug):
    city = City.query.filter_by(slug=slug).first_or_404()

    vendors = (
        Vendor.query
        .filter_by(city_id=city.id)
        .order_by(Vendor.avg_rating.desc().nullslast())
        .all()
    )

    vendor_data = [
        {
            "name": v.name,
            "cuisine_type": v.cuisine_type,
            "rating": v.avg_rating,
            "lat": v.lat,
            "lng": v.lng,
            "address": v.address_text,
            "is_hidden_gem": v.is_hidden_gem,
            "is_famous": v.is_famous,
            "price_level": v.price_level,
        }
        for v in vendors
    ]

    # ✅ ML PART (correct indentation)
    vendor_list = [
        {
            "name": v.name,
            "cuisine_type": v.cuisine_type,
            "description": getattr(v, "description", "") or "",
            "rating": v.avg_rating or 0,
            "price_level": convert_price(v.price_level)
        }
        for v in vendors
    ]

    # Convert list of dicts to tuple of tuples for caching
    vendor_list_tuple = tuple(tuple(d.items()) for d in vendor_list)
    recommendations = get_cached_recommendations(city.id, vendor_list_tuple)

    return render_template(
        "city.html",
        city=city,
        vendors=vendors,
        vendor_data=vendor_data,
        recommendations=recommendations,
        google_maps_api_key=current_app.config.get("GOOGLE_MAPS_API_KEY"),
    )

# -------------------- SUBMIT VENDOR --------------------
@main_bp.route("/submit-vendor", methods=["GET", "POST"])
def submit_vendor():
    cities = City.query.order_by(City.name).all()

    if request.method == "POST":
        city_id = int(request.form.get("city_id"))
        stall_name = request.form.get("stall_name")
        cuisine_type = request.form.get("cuisine_type")
        description = request.form.get("description")
        google_maps_url = request.form.get("google_maps_url")
        approx_address = request.form.get("approx_address")
        estimated_price = request.form.get("estimated_price")
        submitted_by_name = request.form.get("submitted_by_name")
        submitted_by_email = request.form.get("submitted_by_email")

        lat = None
        lng = None

        try:
            if google_maps_url:

                # Case 1: @lat,lng
                match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', google_maps_url)
                if match:
                    lat = float(match.group(1))
                    lng = float(match.group(2))

                # Case 2: !3dLAT!4dLNG
                if lat is None:
                    match = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', google_maps_url)
                    if match:
                        lat = float(match.group(1))
                        lng = float(match.group(2))

                # Case 3: q=lat,lng
                if lat is None and "q=" in google_maps_url:
                    coords = google_maps_url.split("q=")[-1].split("&")[0]
                    parts = coords.split(",")
                    if len(parts) == 2:
                        lat = float(parts[0])
                        lng = float(parts[1])

        except Exception as e:
            print("Map parsing failed:", e)

        submission = VendorSubmission(
            city_id=city_id,
            stall_name=stall_name,
            cuisine_type=cuisine_type,
            description=description,
            google_maps_url=google_maps_url,
            approx_address=approx_address,
            estimated_price=estimated_price,
            submitted_by_name=submitted_by_name,
            submitted_by_email=submitted_by_email,
            lat=lat,
            lng=lng,
        )

        db.session.add(submission)
        db.session.commit()

        flash("✅ Thank you! Your hidden stall suggestion is submitted.", "success")
        return redirect(url_for("main.index"))

    return render_template("submit_vendor.html", cities=cities)