import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///"
    + os.path.join(os.path.dirname(os.path.dirname(__file__)), "contentops.db"),
)

CONTENT_ROOT = os.getenv(
    "CONTENT_ROOT",
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "clients"),
)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme-in-production")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# Google OAuth settings
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
ALLOWED_DOMAINS = ["searchatlas.com", "linkgraph.io"]
