import os
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
from datetime import datetime

from config import SQLALCHEMY_DATABASE_URI, STATIC_IMAGES_PATH, SECRET_KEY
from database import db
from extensions import limiter
from routes.admin import admin_bp
from services.booking import BookingService


app = Flask(__name__)

app.secret_key = SECRET_KEY
app.register_blueprint(admin_bp)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config.update(
    SECRET_KEY=SECRET_KEY,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)
)

db.init_app(app)

with app.app_context():
    db.create_all()

csrf = CSRFProtect(app)
limiter.init_app(app)


@app.route('/')
def index():
    service_coverage_images_path = STATIC_IMAGES_PATH / "affiliations"
    service_coverage_images = os.listdir(service_coverage_images_path)
    return render_template('index.html', title='Home Page', service_coverage_images=service_coverage_images)

@app.route('/booking', methods=['GET'])
def booking_page():
    """Renders the dedicated appointment booking page."""
    return render_template('booking.html', title='Book Appointment')

@app.route('/about', methods=['GET'])
def about_page():
    """Renders the about us page."""
    return render_template('about.html', title='About Us')

@app.route('/services', methods=['GET'])
def services_page():
    """Renders the services page."""
    return render_template('services.html', title='Our Services')

@app.route('/faqs', methods=['GET'])
def faqs_page():
    """Renders the FAQs page."""
    return render_template('faqs.html', title='FAQs')

@app.route('/referrers', methods=['GET'])
def referrers_page():
    """Renders the referrers page."""
    return render_template('referrers.html', title='Referrers')

@app.route('/contact', methods=['GET'])
def contact_page():
    """Renders the contact page."""
    return render_template('contact.html', title='Contact Us')

@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    """Handles the form submission for booking."""
    form = request.form

    relationship_to_client = form.get("relationship_to_client", "").strip()
    client_full_name = form.get("client_full_name", "").strip()
    client_gender = form.get("client_gender", "").strip()
    client_dob = form.get("client_dob", "").strip()
    phone_number = form.get("phone_number", "").strip()
    email = form.get("email", "").strip()
    suburb = form.get("suburb", "").strip()
    resident_type = form.get("resident_type", "").strip()
    referral_type = form.get("referral_type", "").strip()
    ndis_number = form.get("ndis_number", "").strip() or None
    client_concern = form.get("client_concern", "").strip() or None
    
    form_data = {
        "relationship_to_client": relationship_to_client,
        "client_full_name": client_full_name,
        "client_gender": client_gender,
        "client_dob": client_dob,
        "phone_number": phone_number,
        "email": email,
        "suburb": suburb,
        "resident_type": resident_type,
        "referral_type": referral_type,
        "ndis_number": ndis_number,
        "client_concern": client_concern
    }
    
    booking_service = BookingService()
    booking = booking_service.create_booking(form_data)

    if not booking:
        return "<h1>Failed to create booking request</h1>"

    return render_template('booking-request-submitted.html')


if __name__ == '__main__':
    app.run(debug=True)