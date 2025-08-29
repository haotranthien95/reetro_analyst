from __future__ import annotations
from typing import Optional
import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row

from passlib.context import CryptContext
import jwt

from .settings import JWT_SECRET_KEY, JWT_ALGORITHM, DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD

router = APIRouter()
security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"


def ensure_auth_bootstrap(conn: psycopg.Connection) -> None:
    """Ensure pgcrypto, users table, and default admin exist (idempotent)."""
    with conn.cursor() as cur:
        # Ensure pgcrypto for gen_random_uuid()
        cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
        # Users table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS public.users (
                id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
                username text UNIQUE NOT NULL,
                password_hash text NOT NULL,
                role text NOT NULL DEFAULT 'admin',
                is_active boolean NOT NULL DEFAULT true
            )
            """
        )
        # Default admin user
        cur.execute("SELECT 1 FROM public.users WHERE username = %s", (DEFAULT_ADMIN_USERNAME,))
        if cur.fetchone() is None:
            hashed = pwd_context.hash(DEFAULT_ADMIN_PASSWORD)
            cur.execute(
                "INSERT INTO public.users (username, password_hash, role, is_active) VALUES (%s, %s, 'admin', true)",
                (DEFAULT_ADMIN_USERNAME, hashed),
            )
        conn.commit()


def _get_user(conn: psycopg.Connection, username: str) -> Optional[dict]:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            "SELECT id, username, password_hash, role, is_active FROM public.users WHERE username=%s",
            (username,),
        )
        return cur.fetchone()


def create_access_token(username: str, role: str) -> str:
    # No expiration, as requested. Include iat for traceability.
    payload = {"sub": username, "role": role, "iat": int(time.time())}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        # No 'exp' to validate; token never expires by design.
        return payload  # contains at least sub, role
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    # We access the global connection via module import (main initializes it)
    from . import main as app_main
    if app_main.pool is None:
        raise HTTPException(status_code=500, detail="DB pool not initialized")

    user = _get_user(app_main.pool, body.username)
    if not user or not user.get("is_active"):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not pwd_context.verify(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user["username"], user.get("role", "user"))
    return TokenResponse(accessToken=token)