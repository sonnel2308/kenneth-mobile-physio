import logging
import resend
from datetime import datetime, timedelta, timezone
from flask import render_template

from database import db
from config import NOTIFICATION_EMAIL_RECEIVER, NOTIFICATION_EMAIL_SENDER
from models.booking import Booking


logger = logging.getLogger(__name__)

class BookingService():
    def _send_email(self, receiver: str, html_template: str, booking: Booking, verification_url: str = None):
        try:
            resend.Emails.send({
                "from": NOTIFICATION_EMAIL_SENDER,
                "to": receiver,
                "subject": "New Appointment Request Notification",
                "html": render_template(html_template, booking=booking),
            })
        except Exception as e:
            logger.exception(f"Failed to send email notification for {booking.id}: {e}")
    
    def get_bookings(self) -> list[Booking]:
        stmt = db.select(Booking)
        bookings = db.session.execute(stmt).scalars().all()
        
        return bookings
    
    def get_booking(self, id: int) -> Booking | None:
        stmt = db.select(Booking).where(Booking.id == int)
        booking = db.session.execute(stmt).scalar_one_or_none()
        
        if booking is None:
            return None
        
        return booking
    
    def create_booking(self, form_data: dict) -> Booking | None:
        email = form_data["email"]
        
        booking = Booking(**form_data)
        
        try:
            db.session.add(booking)
            db.session.commit()
            logger.info(f"Booking appointment request created: {booking.id}")
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error creating booking appointment request: {e}")
            return None

        self._send_email(NOTIFICATION_EMAIL_RECEIVER, "emails/booking-notification.html", booking)
        self._send_email(email, "emails/client-booking-confirmation.html", booking)
            
        return booking

    def update_booking(self, booking_id: int, data: dict) -> bool:
        stmt = db.select(Booking).where(Booking.id == booking_id)
        booking = db.session.execute(stmt).scalar_one_or_none()
        
        if booking is None:
            return False
        
        for field, value in data.items():
            try:
                setattr(booking, field, value)
            except Exception as e:
                logger.log(f"Failed to update booking {booking_id} with ({field}, {value}): {e}")
                db.session.rollback()
                return False
        
        db.session.commit()
        
        return True
