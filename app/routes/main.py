from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from urllib.parse import urlparse, parse_qs

from app import db
from app.models import City, Vendor, VendorSubmission

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # Show all cities (Jaipur, Delhi, etc.)
    cities = City.query.order_by(City.name).all()
    return render_template("index.html", cities=cities)


@main_bp.route("/city/<slug>")
def city_page(slug):
    city = City.query.filter_by(slug=slug).first_or_404()

    # IMPORTANT: for now, show all vendors for this city
    # (no verified_status filter so your seed data appears)
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

    return render_template(
        "city.html",
        city=city,
        vendors=vendors,
        vendor_data=vendor_data,
        google_maps_api_key=current_app.config.get("GOOGLE_MAPS_API_KEY"),
    )


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

        # Parse links like: https://www.google.com/maps?q=lat,lng
        try:
            if google_maps_url and "maps" in google_maps_url:
                parsed = urlparse(google_maps_url)
                query = parse_qs(parsed.query)
                if "q" in query:
                    coords = query["q"][0].split(",")
                    if len(coords) == 2:
                        lat = float(coords[0].strip())
                        lng = float(coords[1].strip())
        except Exception:
            # If parsing fails, just leave lat/lng as None
            pass

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
        flash("Thank you! Your hidden stall suggestion is submitted for review.", "success")
        return redirect(url_for("main.index"))

    return render_template("submit_vendor.html", cities=cities)
