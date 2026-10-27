import logging
import resend
from datetime import datetime
from flask import render_template

from database import db
from config import NOTIFICATION_EMAIL_RECEIVER, NOTIFICATION_EMAIL_SENDER
from models.booking import Booking


logger = logging.getLogger(__name__)

class BookingService():
    def create_booking(self, relationship_to_client: str, client_full_name: str, client_gender: str, client_dob: datetime, phone_number: str, email: str, suburb: str, resident_type: str, referral_type: str, ndis_number: str, client_concern: str):
        booking = Booking(
            relationship_to_client=relationship_to_client,
            client_full_name=client_full_name,
            client_gender=client_gender,
            client_dob=client_dob,
            phone_number=phone_number,
            email=email,
            suburb=suburb,
            resident_type=resident_type,
            referral_type=referral_type,
            ndis_number=ndis_number,
            client_concern=client_concern
        )
        
        try:
            db.session.add(booking)
            db.session.commit()
            logger.info(f"Booking appointment request created: {booking.id}")
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error creating booking appointment request: {e}")

        try:
            resend.Emails.send({
                "from": NOTIFICATION_EMAIL_SENDER,
                "to": NOTIFICATION_EMAIL_RECEIVER,
                "subject": "New Appointment Request Notification",
                "html": render_template("emails/booking_notification.html", booking=booking)
            })
        except Exception as e:
            logger.excpetion(f"Failed to send email notification for {booking.id}: {e}")
        
        try:
            resend.Emails.send({
                "from": NOTIFICATION_EMAIL_SENDER,
                "to": email,
                "subject": "New Appointment Request Notification",
                "html": render_template("emails/client_booking_confirmation.html", booking=booking)
            })
        except Exception as e:
            logger.exception(f"Failed to send email notification for {booking.id}: {e}")
            
        
        return booking
