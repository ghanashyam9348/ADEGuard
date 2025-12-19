# FastAPI main application
# ADEGuard Backend API - Main FastAPI Application
# Current Date and Time (UTC): 2025-10-17 14:21:01
# Current User's Login: ghanashyam9348
# File: adeguard_backend/app/main.py

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import logging
from contextlib import asynccontextmanager
from pathlib import Path
import sys
import os

# Add app directory to Python path
sys.path.append(str(Path(__file__).parent))

from api.v1.api import api_router
from core.config import settings
from utils.logging_utils import setup_logging
from services.prediction_service import PredictionService

# Global service instances
prediction_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global prediction_service
    
    # Replace emoji lines with plain text versions
    print(f"ADEGuard Backend Starting...")
    print(f"User: ghanashyam9348")
    print(f"Time: 2025-10-17 15:52:34 UTC")
    
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Setting up ADEGuard Backend services...")
        
        # Initialize ML services
        prediction_service = PredictionService()
        await prediction_service.load_models()
        
        logger.info("✅ ADEGuard Backend startup completed successfully")
        yield
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    finally:
        logger.info("🔄 ADEGuard Backend shutting down...")
        if prediction_service:
            await prediction_service.cleanup()
        logger.info("✅ ADEGuard Backend shutdown completed")

# Create FastAPI application
app = FastAPI(
    title="ADEGuard Backend API",
    description="""
    🏥 **ADEGuard Backend API** - Advanced ADE Detection and Reporting System
    
    ## Features:
    - 🔍 **ADE/Drug Span Extraction**: NER-based entity recognition
    - 🎯 **Severity Classification**: ML-powered severity assessment  
    - 📊 **Clustering Analysis**: Age-specific and modifier-aware grouping
    - 💡 **Explainability**: SHAP/LIME model interpretations
    - 🔐 **Secure API**: JWT authentication and role-based access
    - 📱 **Mobile Ready**: Optimized for Android app integration
    
    ## Developed by:
    👤 **User**: ghanashyam9348  
    🕐 **Date**: 2025-10-17 14:21:01 UTC
    
    ## Model Pipeline:
    Steps 1-7 of ADEGuard AI pipeline integrated into production-ready API
    """,
    version="1.0.0",
    contact={
        "name": "ADEGuard Development Team",
        "email": "ghanashyam9348@adeguard.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan
)

# Security
security = HTTPBearer()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Health check endpoints
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API status"""
    return {
        "service": "ADEGuard Backend API",
        "status": "operational",
        "version": "1.0.0",
        "user": "ghanashyam9348",
        "timestamp": "2025-10-17 14:21:01 UTC",
        "message": "🏥 Advanced ADE Detection System - Ready for Production"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    global prediction_service
    
    health_status = {
        "status": "healthy",
        "timestamp": "2025-10-17 14:21:01 UTC",
        "services": {},
        "version": "1.0.0"
    }
    
    # Check ML services
    if prediction_service:
        try:
            service_health = await prediction_service.health_check()
            health_status["services"]["ml_pipeline"] = service_health
        except Exception as e:
            health_status["services"]["ml_pipeline"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "degraded"
    else:
        health_status["services"]["ml_pipeline"] = {
            "status": "not_initialized"
        }
        health_status["status"] = "starting"
    
    return health_status

@app.get("/api/v1/info", tags=["Information"])
async def api_info():
    """API information and capabilities"""
    return {
        "api_name": "ADEGuard Backend",
        "version": "1.0.0",
        "user": "ghanashyam9348",
        "build_date": "2025-10-17 14:21:01 UTC",
        "capabilities": {
            "ner_extraction": "ADE and Drug span identification",
            "severity_classification": "4-class severity assessment (Mild, Moderate, Severe, Life-threatening)",
            "clustering_analysis": "Age-specific and modifier-aware clustering",
            "explainability": "SHAP and LIME model interpretations",
            "real_time_prediction": "Synchronous and asynchronous processing",
            "batch_processing": "Multiple report processing"
        },
        "ml_pipeline_steps": [
            "Step 1: Text Preprocessing",
            "Step 2: NER (ADE/Drug Extraction)", 
            "Step 3: Feature Engineering",
            "Step 4: Clustering Analysis",
            "Step 5: Severity Classification",
            "Step 6: Explainability Generation",
            "Step 7: Response Formatting"
        ],
        "supported_formats": {
            "input": ["text", "structured_form", "json"],
            "output": ["json", "detailed_analysis"]
        },
        "authentication": "JWT Bearer Token",
        "rate_limits": {
            "prediction": "100 requests/minute",
            "batch": "10 requests/minute"
        }
    }

# Exception handlers
# Replace the existing exception handlers with these fixed versions:

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": "2025-10-17 17:29:15 UTC"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    from fastapi.responses import JSONResponse
    logger = logging.getLogger(__name__)
    logger.error(f"Unhandled exception: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500,
            "timestamp": "2025-10-17 17:29:15 UTC",
            "debug": str(exc) if settings.DEBUG else None
        }
    )

# Dependency to get prediction service
async def get_prediction_service() -> PredictionService:
    """Dependency to inject prediction service"""
    global prediction_service
    if not prediction_service:
        raise HTTPException(
            status_code=503, 
            detail="ML services not initialized"
        )
    return prediction_service

if __name__ == "__main__":
    print(f"🚀 Starting ADEGuard Backend API...")
    print(f"👤 User: ghanashyam9348")
    print(f"🕐 Time: 2025-10-17 14:21:01 UTC")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )