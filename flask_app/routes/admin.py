from flask import session, render_template, Blueprint, request, redirect, flash, jsonify
from functools import wraps
from werkzeug.security import check_password_hash

from app import limiter
from config import ADMIN_HASH
from extensions import limiter
from services.booking import BookingService


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_authenticated"):
            return redirect('/admin/login')
        
        return f(*args, **kwargs)
    
    return decorated


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute", methods=['POST'])
def login():
    if session.get("admin_authenticated", False):
        return redirect('/admin/dashboard')
    
    if request.method == 'GET':
        return render_template('admin/login.html')
    
    password = request.form.get("password", "")
    if not check_password_hash(ADMIN_HASH, password):
        flash("Incorrect password", "error")
        return render_template('admin/login.html')
    
    session.clear()
    session["admin_authenticated"] = True
    session.permanent = True
    
    return redirect('/admin/dashboard')

@admin_bp.route("/logout", methods=['POST'])
def logout():
    session.clear()
    flash("Successfully logged out", "success")
    return redirect('/admin/login')

@admin_bp.route("/dashboard", methods=['GET'])
@admin_required
def dashboard():
    booking_service = BookingService()
    bookings = booking_service.get_bookings()

    return render_template('admin/dashboard.html', bookings=bookings)

@admin_bp.route("/bookings/<int:booking_id>", methods=['PATCH', 'DELETE'])
@admin_required
def booking(booking_id: int):
    booking_service = BookingService()
    
    if request.method == 'PATCH':
        data = request.get_json()
        if booking_service.update_booking(booking_id, data):
            return jsonify(status="success", code=200), 200
        
        return jsonify(error="Invalid request"), 400
    elif request.method == 'DELETE':
        if booking_service.delete_booking(booking_id):
            return jsonify(status="success", code=200), 200
        
        return jsonify(error="Invalid request"), 400
