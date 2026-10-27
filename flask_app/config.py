import os
from pathlib import Path

ROOT_PATH = Path(__file__).parent.resolve()
STATIC_PATH = ROOT_PATH / "static"

STATIC_IMAGES_PATH = STATIC_PATH / "images"

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")

NOTIFICATION_EMAIL_SENDER = os.environ.get("NOTIFICATION_EMAIL_SENDER")
NOTIFICATION_EMAIL_RECEIVER = os.environ.get("NOTIFICATION_EMAIL_RECEIVER")
