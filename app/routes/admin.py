from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import VendorSubmission, Vendor

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/submissions")
def admin_submissions():
    submissions = VendorSubmission.query.order_by(VendorSubmission.created_at.desc()).all()
    return render_template("admin_submissions.html", submissions=submissions)


@admin_bp.route("/submissions/<int:submission_id>/approve")
def admin_approve_submission(submission_id):
    sub = VendorSubmission.query.get_or_404(submission_id)

    if sub.status == "approved":
        flash("Already approved.", "info")
        return redirect(url_for("admin.admin_submissions"))

    vendor = Vendor(
        city_id=sub.city_id,
        name=sub.stall_name,
        cuisine_type=sub.cuisine_type,
        is_hidden_gem=True,
        is_famous=False,
        avg_rating=None,
        price_level=sub.estimated_price,
        address_text=sub.approx_address,
        area=None,
        lat=sub.lat if sub.lat else 0.0,
        lng=sub.lng if sub.lng else 0.0,
        source="user",
        verified_status="verified",
    )

    sub.status = "approved"
    db.session.add(vendor)
    db.session.commit()

    flash(f"Vendor '{sub.stall_name}' approved and added.", "success")
    return redirect(url_for("admin.admin_submissions"))


@admin_bp.route("/submissions/<int:submission_id>/reject")
def admin_reject_submission(submission_id):
    sub = VendorSubmission.query.get_or_404(submission_id)
    sub.status = "rejected"
    db.session.commit()
    flash("Submission rejected.", "warning")
    return redirect(url_for("admin.admin_submissions"))
