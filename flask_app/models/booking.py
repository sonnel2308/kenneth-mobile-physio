from datetime import datetime

from database import db


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    relationship_to_client = db.Column(db.Text, nullable=False)
    client_full_name = db.Column(db.Text, nullable=False)
    client_gender = db.Column(db.Text, nullable=False)
    client_dob = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    suburb = db.Column(db.Text, nullable=False)
    resident_type = db.Column(db.Text, nullable=False)
    referral_type = db.Column(db.Text, nullable=False)
    ndis_number = db.Column(db.Text, nullable=True)
    client_concern = db.Column(db.Text, nullable=True)

    status = db.Column(
        db.Text,
        nullable=False,
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now
    )
