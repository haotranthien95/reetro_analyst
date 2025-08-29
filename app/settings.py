from __future__ import annotations
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required. Put it in .env or environment.")

OVERRIDE_KEY_FIELDS: List[str] = [
    f.strip() for f in os.getenv("OVERRIDE_KEY_FIELDS", "ma_dat_hang,ma_hang").split(",") if f.strip()
]

CORS_ALLOW_ORIGINS_RAW = os.getenv("CORS_ALLOW_ORIGINS", "*")
CORS_ALLOW_ORIGINS: List[str] = (
    ["*"] if CORS_ALLOW_ORIGINS_RAW.strip() == "*" else [s.strip() for s in CORS_ALLOW_ORIGINS_RAW.split(",") if s.strip()]
)

# JWT settings
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "CHANGE_ME_DEV_ONLY")
JWT_ALGORITHM: str = "HS256"

DEFAULT_ADMIN_USERNAME: str = os.getenv("DEFAULT_ADMIN_USERNAME", "aaaaaa")
DEFAULT_ADMIN_PASSWORD: str = os.getenv("DEFAULT_ADMIN_PASSWORD", "bbbbbb")  # used once to seed; will be hashed