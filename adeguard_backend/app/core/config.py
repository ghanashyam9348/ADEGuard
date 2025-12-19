# ADEGuard Backend API - Configuration Settings
# Current Date and Time (UTC): 2025-10-17 14:21:01
# Current User's Login: ghanashyam9348
# File: adeguard_backend/app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """ADEGuard Backend Configuration Settings"""
    
    # Basic API Settings
    API_NAME: str = "ADEGuard Backend API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    WORKERS: int = Field(default=1, env="WORKERS")
    
    # Security
    SECRET_KEY: str = Field(
        default="adeguard-secret-key-ghanashyam9348-2025-10-17-14-21-01",
        env="SECRET_KEY"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = "HS256"
    
    # CORS and Security
    ALLOWED_HOSTS: List[str] = Field(
        default=["*"], 
        env="ALLOWED_HOSTS"
    )
    CORS_ORIGINS: List[str] = Field(
        default=["*"],
        env="CORS_ORIGINS"
    )
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="sqlite:///./adeguard.db",
        env="DATABASE_URL"
    )
    
    # ML Model Paths
    BASE_MODEL_PATH: Path = Field(
        default=Path("saved_models"),
        env="BASE_MODEL_PATH"
    )
    
    # NER Model Settings
    NER_MODEL_PATH: str = Field(
        default="saved_models/ner_model",
        env="NER_MODEL_PATH"
    )
    NER_MODEL_NAME: str = Field(
        default="dmis-lab/biobert-base-cased-v1.1",
        env="NER_MODEL_NAME"
    )
    
    # Severity Classification Model
    SEVERITY_MODEL_PATH: str = Field(
        default="saved_models/severity_model",
        env="SEVERITY_MODEL_PATH"
    )
    
    # Clustering Model Settings
    CLUSTERING_MODEL_PATH: str = Field(
        default="saved_models/clustering_model",
        env="CLUSTERING_MODEL_PATH"
    )
    
    # Explainability Settings
    EXPLAINABILITY_MODEL_PATH: str = Field(
        default="saved_models/explainability_models",
        env="EXPLAINABILITY_MODEL_PATH"
    )
    ENABLE_SHAP: bool = Field(default=True, env="ENABLE_SHAP")
    ENABLE_LIME: bool = Field(default=True, env="ENABLE_LIME")
    
    # Processing Settings
    MAX_TEXT_LENGTH: int = Field(default=10000, env="MAX_TEXT_LENGTH")
    BATCH_SIZE: int = Field(default=32, env="BATCH_SIZE")
    MAX_BATCH_REPORTS: int = Field(default=50, env="MAX_BATCH_REPORTS")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=100, env="RATE_LIMIT_PER_MINUTE")
    BATCH_RATE_LIMIT: int = Field(default=10, env="BATCH_RATE_LIMIT")
    
    # Caching
    ENABLE_CACHING: bool = Field(default=True, env="ENABLE_CACHING")
    CACHE_TTL: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Background Tasks
    ENABLE_BACKGROUND_TASKS: bool = Field(default=True, env="ENABLE_BACKGROUND_TASKS")
    MAX_BACKGROUND_TASKS: int = Field(default=10, env="MAX_BACKGROUND_TASKS")
    
    # Model Performance Monitoring
    ENABLE_MONITORING: bool = Field(default=True, env="ENABLE_MONITORING")
    METRICS_EXPORT_PORT: int = Field(default=8001, env="METRICS_EXPORT_PORT")
    
    # Feature Flags
    ENABLE_NER: bool = Field(default=True, env="ENABLE_NER")
    ENABLE_CLUSTERING: bool = Field(default=True, env="ENABLE_CLUSTERING") 
    ENABLE_SEVERITY_CLASSIFICATION: bool = Field(default=True, env="ENABLE_SEVERITY_CLASSIFICATION")
    ENABLE_EXPLAINABILITY: bool = Field(default=True, env="ENABLE_EXPLAINABILITY")
    
    # Development Settings
    DEVELOPER: str = "ghanashyam9348"
    BUILD_TIMESTAMP: str = "2025-10-17 14:21:01 UTC"
    
    # Model Confidence Thresholds
    NER_CONFIDENCE_THRESHOLD: float = Field(default=0.8, env="NER_CONFIDENCE_THRESHOLD")
    SEVERITY_CONFIDENCE_THRESHOLD: float = Field(default=0.7, env="SEVERITY_CONFIDENCE_THRESHOLD")
    CLUSTERING_MIN_SAMPLES: int = Field(default=5, env="CLUSTERING_MIN_SAMPLES")
    
    # API Response Settings
    INCLUDE_DEBUG_INFO: bool = Field(default=False, env="INCLUDE_DEBUG_INFO")
    INCLUDE_PROCESSING_TIME: bool = Field(default=True, env="INCLUDE_PROCESSING_TIME")
    INCLUDE_MODEL_VERSIONS: bool = Field(default=True, env="INCLUDE_MODEL_VERSIONS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

# Global settings instance
settings = Settings()

# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings"""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    INCLUDE_DEBUG_INFO: bool = True
    ENABLE_MONITORING: bool = False

class ProductionSettings(Settings):
    """Production environment settings"""
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    INCLUDE_DEBUG_INFO: bool = False
    WORKERS: int = 4
    ALLOWED_HOSTS: List[str] = ["adeguard-api.com", "api.adeguard.com"]

class TestingSettings(Settings):
    """Testing environment settings"""
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test_adeguard.db"
    ENABLE_BACKGROUND_TASKS: bool = False
    ENABLE_MONITORING: bool = False

def get_settings(environment: str = None) -> Settings:
    """Get settings based on environment"""
    
    if not environment:
        environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()

# Print configuration summary
def print_config_summary():
    """Print configuration summary for debugging"""
    print(f"\n🔧 ADEGuard Backend Configuration Summary:")
    print(f"   👤 Developer: {settings.DEVELOPER}")
    print(f"   🕐 Build Time: {settings.BUILD_TIMESTAMP}")
    print(f"   🌐 Host: {settings.HOST}:{settings.PORT}")
    print(f"   🐛 Debug Mode: {settings.DEBUG}")
    print(f"   📊 ML Features Enabled:")
    print(f"      - NER: {settings.ENABLE_NER}")
    print(f"      - Clustering: {settings.ENABLE_CLUSTERING}")
    print(f"      - Severity: {settings.ENABLE_SEVERITY_CLASSIFICATION}")
    print(f"      - Explainability: {settings.ENABLE_EXPLAINABILITY}")
    print(f"   📁 Model Paths:")
    print(f"      - Base: {settings.BASE_MODEL_PATH}")
    print(f"      - NER: {settings.NER_MODEL_PATH}")
    print(f"      - Severity: {settings.SEVERITY_MODEL_PATH}")
    print(f"   ⚡ Performance:")
    print(f"      - Rate Limit: {settings.RATE_LIMIT_PER_MINUTE}/min")
    print(f"      - Batch Size: {settings.BATCH_SIZE}")
    print(f"      - Cache TTL: {settings.CACHE_TTL}s")

if __name__ == "__main__":
    print_config_summary()