from flask import Flask, render_template, request
import os

from config import STATIC_IMAGES_PATH


app = Flask(__name__)

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

@app.route('/referral', methods=['GET'])
def referral_page():
    """Renders the referral form page."""
    return render_template('making-a-referral.html', title='Making a Referral')

@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    """Handles the form submission for booking."""
    # In a real application, validation and database insertion would happen here.
    full_name = request.form.get('full_name')
    phone = request.form.get('phone_number')
    email = request.form.get('email')
    
    # For now, we just confirm receipt and redirect back to the booking page or success page.
    print(f"Booking submission received: Name={full_name}, Phone={phone}, Email={email}")
    
    # Redirect back to the booking page to show success message or just stay on the page
    return render_template('booking.html', 
                           title='Booking Confirmed', 
                           success=True, 
                           name=full_name)

if __name__ == '__main__':
    app.run(debug=True)