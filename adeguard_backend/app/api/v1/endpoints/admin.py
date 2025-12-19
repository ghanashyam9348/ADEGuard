# Admin functions
# ADEGuard Backend API - Administration Endpoints
# Current Date and Time (UTC): 2025-10-17 15:34:01
# Current User's Login: ghanashyam9348

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
import logging
from datetime import datetime

from app.dependencies import get_current_user, get_prediction_service
from app.services.prediction_service import PredictionService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/system/status")
async def get_system_status(
    prediction_service: PredictionService = Depends(get_prediction_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    🖥️ Get comprehensive system status
    
    **User**: ghanashyam9348  
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    # Check if user has admin role
    if current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    try:
        health_status = await prediction_service.health_check()
        
        return {
            "system_status": "operational",
            "timestamp": "2025-10-17 15:34:01 UTC",
            "admin_user": current_user['username'],
            "services": health_status.get('services', {}),
            "uptime": health_status.get('initialization_time', 0),
            "version": "1.0.0",
            "environment": "development"
        }
        
    except Exception as e:
        logger.error(f"❌ System status check failed: {e}")
        return {
            "system_status": "degraded",
            "timestamp": "2025-10-17 15:34:01 UTC",
            "error": str(e)
        }

@router.post("/models/reload")
async def reload_models(
    prediction_service: PredictionService = Depends(get_prediction_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    🔄 Reload ML models (admin only)
    
    **User**: ghanashyam9348  
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    if current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    try:
        await prediction_service.load_models()
        
        return {
            "message": "Models reloaded successfully",
            "timestamp": "2025-10-17 15:34:01 UTC",
            "admin_user": current_user['username'],
            "reload_successful": True
        }
        
    except Exception as e:
        logger.error(f"❌ Model reload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model reload failed: {str(e)}"
        )

@router.get("/logs")
async def get_system_logs(
    lines: int = 100,
    level: str = "INFO",
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    📋 Get system logs (admin only)
    
    **User**: ghanashyam9348  
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    if current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return {
        "message": f"System logs (last {lines} lines, level: {level})",
        "timestamp": "2025-10-17 15:34:01 UTC",
        "admin_user": current_user['username'],
        "logs": [
            "2025-10-17 15:34:01 INFO: ADEGuard Backend started",
            "2025-10-17 15:34:01 INFO: Models loaded successfully",
            "2025-10-17 15:34:01 INFO: API endpoints registered"
        ],
        "note": "Log file integration to be implemented"
    }

@router.get("/users")
async def list_users(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    👥 List all users (admin only)
    
    **User**: ghanashyam9348  
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    if current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return {
        "users": [
            {
                "username": "ghanashyam9348",
                "role": "admin",
                "created": "2025-10-17 15:34:01 UTC",
                "last_login": "2025-10-17 15:34:01 UTC",
                "active": True
            }
        ],
        "total_users": 1,
        "timestamp": "2025-10-17 15:34:01 UTC",
        "admin_user": current_user['username']
    }

@router.get("/metrics")
async def get_system_metrics(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    📊 Get system performance metrics (admin only)
    
    **User**: ghanashyam9348  
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    if current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return {
        "metrics": {
            "total_predictions": 0,
            "predictions_today": 0,
            "average_response_time": "0.0s",
            "error_rate": "0%",
            "uptime": "100%"
        },
        "timestamp": "2025-10-17 15:34:01 UTC",
        "admin_user": current_user['username'],
        "note": "Metrics collection to be implemented with database"
    }