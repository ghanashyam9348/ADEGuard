# Logging setup
# ADEGuard Backend API - Logging Utilities
# Current Date and Time (UTC): 2025-10-17 14:37:50
# Current User's Login: ghanashyam9348

import logging
import sys
from pathlib import Path

def setup_logging():
    """Setup structured logging for ADEGuard Backend"""
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Setup root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logs_dir / "adeguard_backend.log")
        ]
    )
    
    # Setup specific loggers
    logger = logging.getLogger("adeguard")
    logger.info("✅ ADEGuard Backend logging initialized")
    logger.info("👤 User: ghanashyam9348")
    logger.info("🕐 Time: 2025-10-17 14:37:50 UTC")
    
    return logger