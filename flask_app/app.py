from flask import Flask, render_template
from flask import request # Need to import request to process form data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Home Page')

@app.route('/booking', methods=['GET'])
def booking_page():
    """Renders the dedicated appointment booking page."""
    return render_template('booking.html', title='Book Appointment')

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