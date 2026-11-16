import resend
import logging
from flask import render_template

from config import NOTIFICATION_EMAIL_RECEIVER, NOTIFICATION_EMAIL_SENDER


logger = logging.getLogger(__name__)

def send_email(receiver: str, html_template: str, subject: str, **kwargs):
    try:
        resend.Emails.send({
            "from": NOTIFICATION_EMAIL_SENDER,
            "to": receiver or NOTIFICATION_EMAIL_RECEIVER,
            "subject": subject,
            "html": render_template(html_template, **kwargs)
        })
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

