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

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=datetime.now
    )
    
    client_contact = db.Column(db.Text, nullable=False, default="awaiting")

    comments = db.Column(db.Text, nullable=True)
    
    @property
    def is_closed(self):
        return self.client_contact in {"visited", "no_contact", "cancelled"}
    
    __table_args__ = (
        db.CheckConstraint(
            "client_contact IN ('awaiting', 'scheduled', 'visited', 'no_contact', 'cancelled')",
            name="valid_client_contact"
        ),
        db.CheckConstraint(
            "client_gender IN ('male', 'female')",
            name="valid_gender"
        ),
        db.CheckConstraint(
            "resident_type IN ('private resident', 'supported independent living', 'group home', 'aged care', 'other')",
            name="valid_resident_type"
        ),
        db.CheckConstraint(
            "referral_type IN ('support at home', 'ndis', 'wc ctp', 'chronic condition', 'private health insurance', 'not sure')",
            name="valid_referral_type"
        ),
        db.CheckConstraint(
            "relationship_to_client IN ('client', 'general practitioner', 'family member / support coordinator / case manager / carer')",
            name="valid_relationship_to_client"
        ),
    )
