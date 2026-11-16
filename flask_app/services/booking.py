import logging

from database import db
from models.booking import Booking
from utils import send_email


logger = logging.getLogger(__name__)

class BookingService():
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

        send_email(None, "emails/booking-notification.html", f"[BOOKING REQUEST] {booking.client_full_name}", booking=booking)
        send_email(email, "emails/client-booking-confirmation.html", "We've received your booking request", booking=booking)
            
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

    def delete_booking(self, booking_id: int) -> bool:
        stmt = db.delete(Booking).where(Booking.id == booking_id)
        try:
            db.session.execute(stmt)
            db.session.commit()
            return True
        except Exception as e:
            logger.log(f"Failed to delete booking {booking_id}: {e}")
            db.session.rollback()
            return False
