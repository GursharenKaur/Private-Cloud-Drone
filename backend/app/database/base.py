from app.database.database import Base

# Import all models so SQLAlchemy can discover them
from app.models.user import User
from app.models.device import Device
from app.models.video import Video
from app.models.image import Image
from app.models.telemetry import Telemetry
from app.models.login_attempt import LoginAttempt