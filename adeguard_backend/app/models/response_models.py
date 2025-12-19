# ADEGuard Backend API - Response Models
# Current Date and Time (UTC): 2025-10-17 15:17:36
# Current User's Login: ghanashyam9348

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from .request_models import SeverityLevel

class EntitySpan(BaseModel):
    """Named entity span model for extracted ADE/Drug entities"""
    
    text: str = Field(description="Extracted entity text")
    label: str = Field(description="Entity label (ADE, DRUG, MODIFIER)")
    start: int = Field(description="Start character position in text")
    end: int = Field(description="End character position in text")
    confidence: float = Field(
        ge=0.0, 
        le=1.0, 
        description="Confidence score for entity extraction"
    )
    entity_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for this entity"
    )
    normalized_text: Optional[str] = Field(
        default=None,
        description="Normalized/standardized form of the entity"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "text": "severe headache",
                "label": "ADE",
                "start": 45,
                "end": 59,
                "confidence": 0.94,
                "entity_id": "ade_001",
                "normalized_text": "headache_severe"
            }
        }

class SeverityPrediction(BaseModel):
    """Severity classification result"""
    
    predicted_severity: SeverityLevel = Field(description="Predicted severity level")
    confidence: float = Field(
        ge=0.0,
        le=1.0, 
        description="Prediction confidence score"
    )
    severity_probabilities: Dict[str, float] = Field(
        description="Probability distribution across all severity levels"
    )
    prediction_method: str = Field(
        description="Method used for prediction (ml_model, rule_based, hybrid)"
    )
    risk_factors: List[str] = Field(
        default_factory=list,
        description="Identified risk factors that influenced severity prediction"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "predicted_severity": "moderate",
                "confidence": 0.87,
                "severity_probabilities": {
                    "mild": 0.05,
                    "moderate": 0.87,
                    "severe": 0.07,
                    "life_threatening": 0.01
                },
                "prediction_method": "ml_model",
                "risk_factors": ["fever_high_grade", "elderly_patient"]
            }
        }

class ClusterAnalysis(BaseModel):
    """Clustering analysis result"""
    
    cluster_id: int = Field(description="Assigned cluster ID")
    cluster_label: str = Field(description="Human-readable cluster description")
    cluster_size: int = Field(description="Number of reports in this cluster")
    similarity_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Similarity to cluster centroid"
    )
    age_group_distribution: Dict[str, int] = Field(
        description="Age group distribution in cluster"
    )
    severity_distribution: Dict[str, int] = Field(
        description="Severity distribution in cluster"
    )
    common_symptoms: List[str] = Field(
        default_factory=list,
        description="Most common symptoms in this cluster"
    )
    cluster_characteristics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional cluster characteristics"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "cluster_id": 7,
                "cluster_label": "Moderate post-vaccination systemic reactions",
                "cluster_size": 234,
                "similarity_score": 0.78,
                "age_group_distribution": {
                    "adult_18_64": 156,
                    "elderly_65_plus": 45,
                    "teen_13_17": 23,
                    "child_3_12": 10
                },
                "severity_distribution": {
                    "mild": 89,
                    "moderate": 134,
                    "severe": 11
                },
                "common_symptoms": ["fever", "headache", "fatigue", "muscle_aches"],
                "cluster_characteristics": {
                    "avg_onset_hours": 8.5,
                    "avg_duration_days": 2.3,
                    "hospitalization_rate": 0.02
                }
            }
        }

class ExplainabilityResult(BaseModel):
    """Model explainability results from SHAP/LIME"""
    
    shap_values: Optional[Dict[str, Any]] = Field(
        default=None,
        description="SHAP feature importance values"
    )
    lime_explanation: Optional[Dict[str, Any]] = Field(
        default=None,
        description="LIME local explanations"
    )
    top_features: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Top contributing features with importance scores"
    )
    explanation_text: str = Field(
        description="Human-readable explanation of the prediction"
    )
    confidence_factors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Factors that increase or decrease prediction confidence"
    )
    alternative_predictions: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Alternative predictions with their explanations"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "explanation_text": "Severity classified as moderate primarily due to presence of 'high fever' (importance: 0.45) and 'muscle aches' (importance: 0.32). Patient age group (adult) and timing of onset also contributed to this classification.",
                "top_features": [
                    {
                        "feature": "fever_high_grade",
                        "importance": 0.45,
                        "direction": "increases_severity"
                    },
                    {
                        "feature": "muscle_aches",
                        "importance": 0.32,
                        "direction": "increases_severity"
                    },
                    {
                        "feature": "age_adult",
                        "importance": 0.18,
                        "direction": "neutral"
                    }
                ],
                "confidence_factors": [
                    {
                        "factor": "clear_symptom_description",
                        "impact": "increases_confidence",
                        "weight": 0.2
                    }
                ]
            }
        }

class ProcessingMetrics(BaseModel):
    """Processing performance metrics"""
    
    total_processing_time: float = Field(description="Total processing time in seconds")
    ner_processing_time: float = Field(description="NER processing time in seconds")
    clustering_time: float = Field(description="Clustering analysis time in seconds")
    severity_classification_time: float = Field(description="Severity classification time in seconds")
    explainability_time: float = Field(description="Explainability generation time in seconds")
    
    # Additional metrics
    text_preprocessing_time: Optional[float] = Field(
        default=None,
        description="Text preprocessing time in seconds"
    )
    model_inference_time: Optional[float] = Field(
        default=None,
        description="Combined model inference time in seconds"
    )
    response_formatting_time: Optional[float] = Field(
        default=None,
        description="Response formatting time in seconds"
    )
    
    # Resource usage
    memory_usage_mb: Optional[float] = Field(
        default=None,
        description="Peak memory usage in megabytes"
    )
    cpu_usage_percent: Optional[float] = Field(
        default=None,
        description="CPU usage percentage during processing"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "total_processing_time": 2.34,
                "ner_processing_time": 0.45,
                "clustering_time": 0.12,
                "severity_classification_time": 0.67,
                "explainability_time": 0.89,
                "text_preprocessing_time": 0.08,
                "model_inference_time": 1.12,
                "response_formatting_time": 0.13,
                "memory_usage_mb": 245.6,
                "cpu_usage_percent": 23.4
            }
        }

class ModelVersions(BaseModel):
    """Model version information"""
    
    ner_model_version: str = Field(description="NER model version")
    severity_model_version: str = Field(description="Severity classification model version")
    clustering_model_version: str = Field(description="Clustering model version")
    explainability_model_version: str = Field(description="Explainability model version")
    api_version: str = Field(description="API version")
    
    # Additional version info
    model_build_date: Optional[str] = Field(
        default=None,
        description="Date when models were last trained/updated"
    )
    model_accuracy_metrics: Optional[Dict[str, float]] = Field(
        default=None,
        description="Latest accuracy metrics for models"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "ner_model_version": "biobert-adeguard-v2.1",
                "severity_model_version": "severity-classifier-v1.3",
                "clustering_model_version": "hdbscan-embeddings-v1.0",
                "explainability_model_version": "shap-lime-v1.2",
                "api_version": "1.0.0",
                "model_build_date": "2025-10-15",
                "model_accuracy_metrics": {
                    "ner_f1_score": 0.91,
                    "severity_accuracy": 0.84,
                    "clustering_silhouette": 0.67
                }
            }
        }

class AlertInfo(BaseModel):
    """Detailed alert information"""
    
    alert_id: str = Field(description="Unique alert identifier")
    alert_type: str = Field(description="Type of alert (critical, warning, info)")
    message: str = Field(description="Alert message")
    severity_level: str = Field(description="Alert severity level")
    recommended_actions: List[str] = Field(
        default_factory=list,
        description="Recommended actions for this alert"
    )
    timestamp: datetime = Field(description="Alert generation timestamp")
    auto_notify: bool = Field(
        default=False,
        description="Whether this alert should trigger automatic notifications"
    )
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "alert_id": "alert_critical_001",
                "alert_type": "critical",
                "message": "Life-threatening ADE detected - Immediate medical attention required",
                "severity_level": "life_threatening",
                "recommended_actions": [
                    "Contact emergency services immediately",
                    "Discontinue suspected medication",
                    "Monitor vital signs continuously"
                ],
                "timestamp": "2025-10-17T15:17:36Z",
                "auto_notify": True
            }
        }

class ADEReportResponse(BaseModel):
    """Complete ADE report analysis response"""
    
    # Request tracking
    request_id: str = Field(description="Unique request identifier")
    timestamp: datetime = Field(description="Response timestamp")
    processing_status: str = Field(
        default="completed",
        description="Processing status (completed, partial, failed)"
    )
    
    # Analysis results
    extracted_entities: List[EntitySpan] = Field(
        description="Extracted ADE/Drug entities"
    )
    severity_analysis: SeverityPrediction = Field(
        description="Severity classification results"
    )
    cluster_analysis: Optional[ClusterAnalysis] = Field(
        default=None,
        description="Clustering analysis results"
    )
    explainability: Optional[ExplainabilityResult] = Field(
        default=None,
        description="Model explainability results"
    )
    
    # Summary information
    summary: Dict[str, Any] = Field(
        description="High-level summary of analysis results"
    )
    
    # Metadata
    processing_metrics: Optional[ProcessingMetrics] = Field(
        default=None,
        description="Processing performance metrics"
    )
    model_versions: Optional[ModelVersions] = Field(
        default=None,
        description="Model version information"
    )
    
    # Alerts and recommendations
    alerts: List[Union[str, AlertInfo]] = Field(
        default_factory=list,
        description="Critical alerts based on analysis"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Clinical recommendations"
    )
    
    # Additional response data
    similar_cases: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Similar cases from historical data"
    )
    regulatory_info: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Relevant regulatory information"
    )
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "request_id": "req_20251017151736_abc123",
                "timestamp": "2025-10-17T15:17:36Z",
                "processing_status": "completed",
                "summary": {
                    "severity_level": "moderate",
                    "ade_entities_found": 3,
                    "drug_entities_found": 1,
                    "total_entities": 4,
                    "requires_attention": True,
                    "cluster_assigned": True
                },
                "alerts": [
                    "⚠️ MODERATE: Moderate ADE detected - Medical evaluation recommended"
                ],
                "recommendations": [
                    "Monitor patient closely for symptom progression",
                    "Consider dose adjustment or alternative medication",
                    "Schedule follow-up within 24-48 hours"
                ]
            }
        }

class BatchADEResponse(BaseModel):
    """Batch processing response"""
    
    batch_id: str = Field(description="Batch processing identifier")
    timestamp: datetime = Field(description="Batch completion timestamp")
    batch_status: str = Field(
        description="Overall batch status (completed, partial, failed)"
    )
    
    # Individual results
    individual_results: Optional[List[ADEReportResponse]] = Field(
        default=None,
        description="Results for each individual report"
    )
    
    # Batch summary
    batch_summary: Dict[str, Any] = Field(
        description="Batch-level summary statistics"
    )
    
    # Processing information
    total_reports_processed: int = Field(description="Number of reports processed")
    successful_reports: int = Field(description="Number of successfully processed reports")
    failed_reports: int = Field(description="Number of failed reports")
    total_processing_time: float = Field(description="Total batch processing time")
    
    # Batch-level analytics
    severity_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="Distribution of severity levels across batch"
    )
    alert_summary: Dict[str, int] = Field(
        default_factory=dict,
        description="Summary of alerts generated across batch"
    )
    top_entities: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Most frequently extracted entities across batch"
    )
    
    # Errors and warnings
    errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Errors encountered during batch processing"
    )
    warnings: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Warnings generated during batch processing"
    )
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "batch_id": "batch_20251017151736_ghanashyam9348",
                "timestamp": "2025-10-17T15:17:36Z",
                "batch_status": "completed",
                "total_reports_processed": 25,
                "successful_reports": 23,
                "failed_reports": 2,
                "total_processing_time": 45.67,
                "batch_summary": {
                    "success_rate": 0.92,
                    "average_processing_time": 1.98,
                    "total_entities_extracted": 127,
                    "critical_alerts_generated": 3
                },
                "severity_distribution": {
                    "mild": 8,
                    "moderate": 12,
                    "severe": 3,
                    "life_threatening": 0
                },
                "alert_summary": {
                    "critical": 3,
                    "warning": 7,
                    "info": 15
                }
            }
        }

class ErrorResponse(BaseModel):
    """Standardized error response model"""
    
    error: bool = Field(default=True, description="Error flag")
    error_code: str = Field(description="Specific error code")
    message: str = Field(description="Human-readable error message")
    status_code: int = Field(description="HTTP status code")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Error timestamp"
    )
    request_id: Optional[str] = Field(
        default=None,
        description="Request ID if available"
    )
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details"
    )
    
    # Error context
    user_id: Optional[str] = Field(
        default=None,
        description="User ID associated with the error"
    )
    endpoint: Optional[str] = Field(
        default=None,
        description="API endpoint where error occurred"
    )
    
    # Troubleshooting information
    suggested_action: Optional[str] = Field(
        default=None,
        description="Suggested action to resolve the error"
    )
    support_reference: Optional[str] = Field(
        default=None,
        description="Support reference ID for tracking"
    )
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "error": True,
                "error_code": "VALIDATION_ERROR",
                "message": "Symptom text must contain at least 10 characters",
                "status_code": 422,
                "timestamp": "2025-10-17T15:17:36Z",
                "request_id": "req_20251017151736_error",
                "details": {
                    "field": "symptom_text",
                    "provided_length": 3,
                    "minimum_required": 10
                },
                "user_id": "ghanashyam9348",
                "endpoint": "/api/v1/predict/single",
                "suggested_action": "Please provide a more detailed description of symptoms",
                "support_reference": "ERR_20251017151736_001"
            }
        }

class HealthResponse(BaseModel):
    """Health check response model"""
    
    status: str = Field(description="Overall health status")
    timestamp: datetime = Field(description="Health check timestamp")
    version: str = Field(description="API version")
    uptime_seconds: float = Field(description="API uptime in seconds")
    
    # Service health
    services: Dict[str, Dict[str, Any]] = Field(
        description="Health status of individual services"
    )
    
    # System metrics
    system_metrics: Optional[Dict[str, Any]] = Field(
        default=None,
        description="System resource metrics"
    )
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-10-17T15:17:36Z",
                "version": "1.0.0",
                "uptime_seconds": 3600.5,
                "services": {
                    "ml_pipeline": {
                        "status": "healthy",
                        "response_time_ms": 234
                    },
                    "database": {
                        "status": "healthy",
                        "connection_pool": "5/10 active"
                    }
                },
                "system_metrics": {
                    "cpu_usage_percent": 15.2,
                    "memory_usage_percent": 34.7,
                    "disk_usage_percent": 67.1
                }
            }
        }

# Export all response models
__all__ = [
    "ADEReportResponse",
    "BatchADEResponse",
    "EntitySpan",
    "SeverityPrediction",
    "ClusterAnalysis", 
    "ExplainabilityResult",
    "ProcessingMetrics",
    "ModelVersions",
    "AlertInfo",
    "ErrorResponse",
    "HealthResponse"
]