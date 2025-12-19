# Authentication
# ADEGuard Backend API - Authentication Endpoints
# Current Date and Time (UTC): 2025-10-17 15:34:01
# Current User's Login: ghanashyam9348

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel  # <-- 1. Import BaseModel
import logging
from datetime import datetime, timedelta

# --- Pydantic Model for Request Body ---
# This tells FastAPI to expect a JSON object with these fields in the request body.
class UserCredentials(BaseModel):
    username: str
    password: str

security = HTTPBearer()
router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/login")
async def login(
    credentials: UserCredentials  # <-- 2. Use the Pydantic model here
):
    """
    🔐 User authentication and JWT token generation
    
    **User**: ghanashyam9348   
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    # 3. Access credentials from the model object
    if credentials.username == "ghanashyam9348" and credentials.password == "adeguard123":
        return {
            "access_token": "mock_jwt_token_ghanashyam9348",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {
                "username": credentials.username,
                "role": "admin",
                "permissions": ["read", "write", "admin"]
            },
            "timestamp": "2025-10-17 15:34:01 UTC"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

@router.post("/logout")
async def logout(
    token: str = Depends(security)
):
    """
    🚪 User logout and token invalidation
    
    **User**: ghanashyam9348   
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    return {
        "message": "Successfully logged out",
        "timestamp": "2025-10-17 15:34:01 UTC",
        "token_invalidated": True
    }

@router.get("/me")
async def get_current_user_info(
    token: str = Depends(security)
):
    """
    👤 Get current user information
    
    **User**: ghanashyam9348   
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    return {
        "user": {
            "username": "ghanashyam9348",
            "role": "admin",
            "permissions": ["read", "write", "admin"],
            "last_login": "2025-10-17 15:34:01 UTC",
            "account_created": "2025-10-17 15:34:01 UTC"
        },
        "timestamp": "2025-10-17 15:34:01 UTC"
    }

@router.post("/refresh")
async def refresh_token(
    token: str = Depends(security)
):
    """
    🔄 Refresh JWT token
    
    **User**: ghanashyam9348   
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    return {
        "access_token": "refreshed_mock_jwt_token_ghanashyam9348",
        "token_type": "bearer",
        "expires_in": 3600,
        "timestamp": "2025-10-17 15:34:01 UTC"
    }