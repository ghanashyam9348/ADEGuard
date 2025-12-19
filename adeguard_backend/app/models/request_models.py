# ADEGuard Backend API - Request Models
# Current Date and Time (UTC): 2025-10-17 15:17:36
# Current User's Login: ghanashyam9348

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class SeverityLevel(str, Enum):
    """Severity level enumeration"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    LIFE_THREATENING = "life_threatening"
    UNKNOWN = "unknown"

class AgeGroup(str, Enum):
    """Age group enumeration"""
    CHILD = "child_3_12"
    TEEN = "teen_13_17"
    ADULT = "adult_18_64"
    ELDERLY = "elderly_65_plus"
    UNKNOWN = "unknown"

class Gender(str, Enum):
    """Gender enumeration"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

class ReporterType(str, Enum):
    """Reporter type enumeration"""
    HEALTHCARE_PROVIDER = "healthcare_provider"
    PATIENT = "patient"
    PHARMACIST = "pharmacist"
    OTHER_HEALTHCARE = "other_healthcare"
    LAWYER = "lawyer"
    CONSUMER = "consumer"

class VaccineType(str, Enum):
    """Common vaccine types"""
    COVID19_MRNA = "covid19_mrna"
    COVID19_VIRAL_VECTOR = "covid19_viral_vector"
    INFLUENZA = "influenza"
    HPV = "hpv"
    HEPATITIS_B = "hepatitis_b"
    MMR = "mmr"
    TDAP = "tdap"
    PNEUMOCOCCAL = "pneumococcal"
    MENINGOCOCCAL = "meningococcal"
    OTHER = "other"

class ADEReportRequest(BaseModel):
    """Main ADE report request model for single report submission"""
    
    # Patient Demographics
    patient_age: Optional[int] = Field(
        default=None, 
        ge=0, 
        le=120, 
        description="Patient age in years"
    )
    age_group: Optional[AgeGroup] = Field(
        default=None,
        description="Patient age group category"
    )
    patient_gender: Optional[Gender] = Field(
        default=None,
        description="Patient gender"
    )
    patient_state: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Patient state/location (US state or country)"
    )
    patient_weight_kg: Optional[float] = Field(
        default=None,
        ge=0.1,
        le=500.0,
        description="Patient weight in kilograms"
    )
    
    # Vaccine/Drug Information
    vaccine_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Name of vaccine administered"
    )
    vaccine_type: Optional[VaccineType] = Field(
        default=None,
        description="Type/category of vaccine"
    )
    vaccine_manufacturer: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Vaccine manufacturer (e.g., Pfizer-BioNTech, Moderna, J&J)"
    )
    vaccine_lot: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Vaccine lot/batch number"
    )
    vaccination_date: Optional[datetime] = Field(
        default=None,
        description="Date and time of vaccination (ISO format)"
    )
    dose_number: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
        description="Dose number (1st, 2nd, booster, etc.)"
    )
    
    # Symptom Information (Core Required Field)
    symptoms: List[str] = Field(
        default_factory=list,
        description="List of structured symptoms (VAERS codes or standard terms)"
    )
    symptom_text: str = Field(
        min_length=10,
        max_length=10000,
        description="Free text description of symptoms and adverse events (REQUIRED)"
    )
    
    # Temporal Information
    onset_date: Optional[datetime] = Field(
        default=None,
        description="Date and time of symptom onset"
    )
    report_date: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Date of report submission"
    )
    days_to_onset: Optional[int] = Field(
        default=None,
        ge=0,
        le=365,
        description="Number of days from vaccination to symptom onset"
    )
    
    # Clinical Outcomes
    hospitalized: Optional[bool] = Field(
        default=None,
        description="Whether patient was hospitalized"
    )
    er_visit: Optional[bool] = Field(
        default=None,
        description="Whether patient visited emergency room"
    )
    life_threatening: Optional[bool] = Field(
        default=None,
        description="Whether event was life-threatening"
    )
    disability: Optional[bool] = Field(
        default=None,
        description="Whether event resulted in disability"
    )
    death: Optional[bool] = Field(
        default=None,
        description="Whether event resulted in death"
    )
    recovery_status: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Patient recovery status (recovered, recovering, not recovered, unknown)"
    )
    
    # Medical History
    prior_vaccinations: Optional[List[str]] = Field(
        default_factory=list,
        description="List of prior vaccinations within last 4 weeks"
    )
    medications: Optional[List[str]] = Field(
        default_factory=list,
        description="Current medications patient is taking"
    )
    allergies: Optional[List[str]] = Field(
        default_factory=list,
        description="Known allergies"
    )
    medical_conditions: Optional[List[str]] = Field(
        default_factory=list,
        description="Pre-existing medical conditions"
    )
    
    # Reporter Information
    reporter_type: Optional[ReporterType] = Field(
        default=None,
        description="Type of person reporting the adverse event"
    )
    reporter_occupation: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Reporter's occupation (if healthcare provider)"
    )
    
    # Processing Options
    include_explainability: bool = Field(
        default=True,
        description="Whether to include SHAP/LIME explanations in response"
    )
    include_clustering: bool = Field(
        default=True,
        description="Whether to include clustering analysis in response"
    )
    confidence_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold for predictions"
    )
    enable_alerts: bool = Field(
        default=True,
        description="Whether to generate clinical alerts for severe cases"
    )
    detailed_metrics: bool = Field(
        default=False,
        description="Whether to include detailed processing metrics"
    )
    
    # Data Quality Flags
    text_language: Optional[str] = Field(
        default="en",
        max_length=5,
        description="Language of symptom text (ISO 639-1 code)"
    )
    data_source: Optional[str] = Field(
        default="api_submission",
        max_length=50,
        description="Source of the data (api_submission, mobile_app, web_form, etc.)"
    )
    
    @validator('symptom_text')
    def validate_symptom_text(cls, v):
        """Validate symptom text is not empty and contains meaningful content"""
        if not v or not v.strip():
            raise ValueError("Symptom text cannot be empty")
        
        # Check for minimum meaningful content
        words = v.strip().split()
        if len(words) < 3:
            raise ValueError("Symptom text must contain at least 3 words")
        
        return v.strip()
    
    @validator('patient_age')
    def validate_age_consistency(cls, v, values):
        """Validate age is consistent with age_group if both provided"""
        if v is not None and 'age_group' in values and values['age_group']:
            age_group = values['age_group']
            age_ranges = {
                AgeGroup.CHILD: (3, 12),
                AgeGroup.TEEN: (13, 17), 
                AgeGroup.ADULT: (18, 64),
                AgeGroup.ELDERLY: (65, 120)
            }
            
            if age_group in age_ranges:
                min_age, max_age = age_ranges[age_group]
                if not (min_age <= v <= max_age):
                    raise ValueError(f"Age {v} is not consistent with age group {age_group}")
        
        return v
    
    @validator('onset_date')
    def validate_onset_after_vaccination(cls, v, values):
        """Validate onset date is after vaccination date if both provided"""
        if v is not None and 'vaccination_date' in values and values['vaccination_date']:
            if v < values['vaccination_date']:
                raise ValueError("Onset date cannot be before vaccination date")
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        use_enum_values = True
        schema_extra = {
            "example": {
                "patient_age": 45,
                "age_group": "adult_18_64",
                "patient_gender": "female",
                "patient_state": "California",
                "patient_weight_kg": 68.5,
                "vaccine_name": "COVID-19 mRNA vaccine",
                "vaccine_type": "covid19_mrna",
                "vaccine_manufacturer": "Pfizer-BioNTech",
                "vaccine_lot": "ABC123",
                "vaccination_date": "2025-10-15T10:00:00Z",
                "dose_number": 2,
                "symptoms": ["fever", "headache", "fatigue", "muscle_aches"],
                "symptom_text": "Patient developed severe headache and high fever (39.5°C) approximately 2 hours after receiving second COVID-19 mRNA vaccination. Also experienced significant fatigue, muscle aches, and chills. Symptoms persisted for 48 hours before gradually improving. No hospitalization required but patient was bedridden for 2 days.",
                "onset_date": "2025-10-15T12:00:00Z",
                "days_to_onset": 0,
                "hospitalized": False,
                "er_visit": False,
                "life_threatening": False,
                "recovery_status": "recovered",
                "prior_vaccinations": ["influenza vaccine 3 weeks ago"],
                "medications": ["ibuprofen as needed"],
                "allergies": ["penicillin"],  
                "medical_conditions": ["hypertension"],
                "reporter_type": "healthcare_provider",
                "reporter_occupation": "registered_nurse",
                "include_explainability": True,
                "include_clustering": True,
                "confidence_threshold": 0.8,
                "enable_alerts": True,
                "text_language": "en",
                "data_source": "mobile_app"
            }
        }

class BatchADERequest(BaseModel):
    """Batch processing request model for multiple reports"""
    
    reports: List[ADEReportRequest] = Field(
        min_items=1,
        max_items=50,
        description="List of ADE reports to process (max 50 per batch)"
    )
    
    # Batch Processing Options
    batch_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Optional name/identifier for this batch"
    )
    parallel_processing: bool = Field(
        default=True,
        description="Whether to process reports in parallel (faster but more resource intensive)"
    )
    fail_fast: bool = Field(
        default=False,
        description="Whether to stop processing on first error or continue with remaining reports"
    )
    
    # Response Options
    return_individual_results: bool = Field(
        default=True,
        description="Whether to return detailed results for each individual report"
    )
    return_batch_summary: bool = Field(
        default=True,
        description="Whether to return batch-level summary statistics"
    )
    return_only_errors: bool = Field(
        default=False,
        description="Whether to return only failed reports (useful for debugging)"
    )
    
    # Processing Overrides (apply to all reports in batch)
    batch_confidence_threshold: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Override confidence threshold for all reports in batch"
    )
    batch_disable_explainability: bool = Field(
        default=False,
        description="Disable explainability for all reports (faster processing)"
    )
    batch_disable_clustering: bool = Field(
        default=False,  
        description="Disable clustering for all reports (faster processing)"
    )
    
    # Metadata
    submitted_by: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Username or identifier of person submitting batch"
    )
    priority: Optional[str] = Field(
        default="normal",
        pattern="^(low|normal|high|urgent)$",
        description="Processing priority level"
    )
    
    @validator('reports')
    def validate_reports_not_empty(cls, v):
        """Ensure reports list is not empty"""
        if not v:
            raise ValueError("Reports list cannot be empty")
        return v
    
    @validator('batch_name')
    def validate_batch_name(cls, v):
        """Validate batch name if provided"""
        if v is not None:
            if not v.strip():
                raise ValueError("Batch name cannot be empty string")
            # Remove special characters that might cause issues
            import re
            if not re.match(r'^[a-zA-Z0-9_\-\s]+$', v):
                raise ValueError("Batch name can only contain letters, numbers, spaces, hyphens, and underscores")
        return v.strip() if v else None
    
    class Config:
        schema_extra = {
            "example": {
                "reports": [
                    {
                        "patient_age": 35,
                        "patient_gender": "male",
                        "vaccine_name": "COVID-19 mRNA vaccine",
                        "vaccine_manufacturer": "Moderna",
                        "symptom_text": "Patient experienced mild fever and fatigue after first COVID vaccination",
                        "hospitalized": False
                    },
                    {
                        "patient_age": 67,
                        "patient_gender": "female", 
                        "vaccine_name": "COVID-19 mRNA vaccine",
                        "vaccine_manufacturer": "Pfizer-BioNTech",
                        "symptom_text": "Severe allergic reaction with difficulty breathing and swelling",
                        "hospitalized": True,
                        "life_threatening": True
                    }
                ],
                "batch_name": "Weekly_Hospital_Reports_Batch_001",
                "parallel_processing": True,
                "return_individual_results": True,
                "return_batch_summary": True,
                "submitted_by": "ghanashyam9348",
                "priority": "normal"
            }
        }

class QuickADERequest(BaseModel):
    """Simplified request model for quick/mobile submissions"""
    
    # Essential fields only
    symptom_text: str = Field(
        min_length=5,
        max_length=5000,
        description="Description of symptoms (required)"
    )
    patient_age: Optional[int] = Field(
        default=None,
        ge=0,
        le=120,
        description="Patient age"
    )
    vaccine_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Vaccine name"
    )
    severity_concern: Optional[str] = Field(
        default=None,
        pattern="^(mild|moderate|severe|emergency)$",
        description="Reporter's assessment of severity"
    )
    
    # Processing options (simplified)
    urgent: bool = Field(
        default=False,
        description="Mark as urgent for priority processing"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "symptom_text": "Had fever and headache after vaccination yesterday",
                "patient_age": 28,
                "vaccine_name": "COVID-19 vaccine",
                "severity_concern": "mild",
                "urgent": False
            }
        }

# Export all request models
__all__ = [
    "ADEReportRequest",
    "BatchADERequest", 
    "QuickADERequest",
    "SeverityLevel",
    "AgeGroup",
    "Gender",
    "ReporterType",
    "VaccineType"
]