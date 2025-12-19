# ADEGuard Backend API - Main API Router
# Current Date and Time (UTC): 2025-10-17 15:34:01
# Current User's Login: ghanashyam9348

from fastapi import APIRouter
from .endpoints import predict, reports, auth, admin

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(predict.router, prefix="/predict", tags=["Prediction"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])  
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(admin.router, prefix="/admin", tags=["Administration"])

@api_router.get("/")
async def api_root():
    """API v1 root endpoint"""
    return {
        "message": "ADEGuard Backend API v1",
        "version": "1.0.0",
        "user": "ghanashyam9348",
        "timestamp": "2025-10-17 15:34:01 UTC",
        "endpoints": {
            "prediction": "/api/v1/predict/",
            "reports": "/api/v1/reports/",
            "authentication": "/api/v1/auth/",
            "administration": "/api/v1/admin/"
        }
    }