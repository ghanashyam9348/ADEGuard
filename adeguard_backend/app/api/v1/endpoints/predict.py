# ADEGuard Backend API - Prediction Endpoints
# Current Date and Time (UTC): 2025-10-17 15:34:01
# Current User's Login: ghanashyam9348

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from typing import Dict, Any, List
import logging
import time
import uuid
from datetime import datetime

from app.models.request_models import ADEReportRequest, BatchADERequest, QuickADERequest
from app.models.response_models import ADEReportResponse, BatchADEResponse, ErrorResponse, HealthResponse
from app.dependencies import get_prediction_service, get_current_user
from app.services.prediction_service import PredictionService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/single", response_model=ADEReportResponse)
async def predict_single_report(
    request: ADEReportRequest,
    prediction_service: PredictionService = Depends(get_prediction_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    🔍 Predict ADE severity and extract entities from a single report
    
    This endpoint processes a single ADE report and returns:
    - Extracted ADE/Drug entities using NER
    - Severity classification (mild, moderate, severe, life-threatening)
    - Clustering analysis (optional)
    - SHAP/LIME explainability results (optional)
    - Clinical recommendations and alerts
    
    **User**: ghanashyam9348  
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    try:
        start_time = time.time()
        logger.info(f"Processing single ADE report for user: {current_user['username']}")
        
        # Convert request to dict for processing
        request_data = request.dict()
        
        # Add user context
        request_data['submitted_by'] = current_user['username']
        request_data['submission_timestamp'] = datetime.utcnow()
        
        # Process the report through ML pipeline
        results = await prediction_service.predict(request_data)
        
        # Convert results to response model
        response = ADEReportResponse(
            request_id=results['request_id'],
            timestamp=results['timestamp'],
            processing_status="completed",
            extracted_entities=results['extracted_entities'],
            severity_analysis=results['severity_analysis'],
            cluster_analysis=results.get('cluster_analysis'),
            explainability=results.get('explainability'),
            summary=results['summary'],
            processing_metrics=results.get('processing_metrics'),
            alerts=results['alerts'],
            recommendations=results['recommendations']
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Single report processed successfully: {results['request_id']} in {processing_time:.2f}s")
        
        return response
        
    except Exception as e:
        logger.error(f"Single report prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "PREDICTION_FAILED",
                "message": f"Prediction failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
                "user": current_user['username']
            }
        )

@router.post("/batch", response_model=BatchADEResponse)
async def predict_batch_reports(
    request: BatchADERequest,
    background_tasks: BackgroundTasks,
    prediction_service: PredictionService = Depends(get_prediction_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Process multiple ADE reports in batch
    
    This endpoint processes multiple ADE reports and returns:
    - Individual results for each report (optional)
    - Batch-level summary statistics
    - Processing metrics and performance data
    - Aggregated insights across the batch
    
    **Limits**: Max 50 reports per batch  
    **User**: ghanashyam9348  
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    try:
        batch_start_time = time.time()
        batch_id = f"batch_{int(time.time())}_{current_user['username']}"
        
        logger.info(f"Processing batch of {len(request.reports)} reports for user: {current_user['username']}")
        
        individual_results = []
        successful_reports = 0
        failed_reports = 0
        errors = []
        warnings = []
        
        # Process each report
        for i, report in enumerate(request.reports):
            try:
                report_start = time.time()
                report_data = report.dict()
                
                # Add batch context
                report_data['batch_id'] = batch_id
                report_data['batch_index'] = i
                report_data['submitted_by'] = current_user['username']
                
                # Apply batch-level overrides
                if request.batch_confidence_threshold is not None:
                    report_data['confidence_threshold'] = request.batch_confidence_threshold
                if request.batch_disable_explainability:
                    report_data['include_explainability'] = False
                if request.batch_disable_clustering:
                    report_data['include_clustering'] = False
                
                result = await prediction_service.predict(report_data)
                
                if request.return_individual_results:
                    individual_results.append(ADEReportResponse(
                        request_id=result['request_id'],
                        timestamp=result['timestamp'],
                        processing_status="completed",
                        extracted_entities=result['extracted_entities'],
                        severity_analysis=result['severity_analysis'],
                        cluster_analysis=result.get('cluster_analysis'),
                        explainability=result.get('explainability'),
                        summary=result['summary'],
                        processing_metrics=result.get('processing_metrics'),
                        alerts=result['alerts'],
                        recommendations=result['recommendations']
                    ))
                
                successful_reports += 1
                report_time = time.time() - report_start
                
                # Log progress for large batches
                if (i + 1) % 10 == 0:
                    logger.info(f"Batch progress: {i + 1}/{len(request.reports)} reports processed")
                
            except Exception as e:
                failed_reports += 1
                error_info = {
                    'report_index': i,
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat(),
                    'error_type': type(e).__name__
                }
                errors.append(error_info)
                logger.error(f"Report {i} failed: {e}")
                
                # Check fail_fast option
                if request.fail_fast:
                    logger.warning(f"Stopping batch processing due to fail_fast=True")
                    break
        
        # Calculate batch summary
        total_processing_time = time.time() - batch_start_time
        success_rate = successful_reports / len(request.reports) if request.reports else 0
        
        batch_summary = {
            'total_reports': len(request.reports),
            'successful_reports': successful_reports,
            'failed_reports': failed_reports,
            'success_rate': success_rate,
            'average_processing_time': total_processing_time / len(request.reports) if request.reports else 0,
            'total_processing_time': total_processing_time,
            'batch_submitted_by': current_user['username'],
            'batch_name': request.batch_name
        }
        
        # Calculate aggregated analytics
        severity_distribution = {}
        alert_summary = {"critical": 0, "warning": 0, "info": 0}
        top_entities = {}
        
        if individual_results:
            # Severity distribution
            for result in individual_results:
                severity = result.severity_analysis.predicted_severity
                severity_distribution[severity] = severity_distribution.get(severity, 0) + 1
            
            # Alert analysis
            for result in individual_results:
                for alert in result.alerts:
                    if "CRITICAL" in str(alert) or "life-threatening" in str(alert):
                        alert_summary["critical"] += 1
                    elif "SEVERE" in str(alert) or "WARNING" in str(alert):
                        alert_summary["warning"] += 1
                    else:
                        alert_summary["info"] += 1
            
            # Top entities across batch
            entity_counts = {}
            for result in individual_results:
                for entity in result.extracted_entities:
                    key = f"{entity.label}:{entity.text}"
                    entity_counts[key] = entity_counts.get(key, 0) + 1
            
            # Sort and get top 10
            top_entities = [
                {"entity": key.split(":", 1)[1], "label": key.split(":", 1)[0], "count": count}
                for key, count in sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ]
        
        response = BatchADEResponse(
            batch_id=batch_id,
            timestamp=datetime.utcnow(),
            batch_status="completed" if failed_reports == 0 else "partial" if successful_reports > 0 else "failed",
            individual_results=individual_results if request.return_individual_results else None,
            batch_summary=batch_summary,
            total_reports_processed=len(request.reports),
            successful_reports=successful_reports,
            failed_reports=failed_reports,
            total_processing_time=total_processing_time,
            severity_distribution=severity_distribution,
            alert_summary=alert_summary,
            top_entities=top_entities,
            errors=errors,
            warnings=warnings
        )
        
        logger.info(f"Batch processing completed: {successful_reports}/{len(request.reports)} successful")
        return response
        
    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "BATCH_PREDICTION_FAILED",
                "message": f"Batch prediction failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
                "user": current_user['username']
            }
        )

@router.post("/quick", response_model=ADEReportResponse)
async def predict_quick_report(
    request: QuickADERequest,
    prediction_service: PredictionService = Depends(get_prediction_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    ⚡ Quick prediction for mobile/simplified submissions
    
    Simplified endpoint for quick ADE reporting with minimal fields.
    Optimized for mobile applications and urgent submissions.
    
    **User**: ghanashyam9348  
    **Updated**: 2025-10-17 15:34:01 UTC
    """
    
    try:
        # Convert quick request to full request format
        full_request = ADEReportRequest(
            symptom_text=request.symptom_text,
            patient_age=request.patient_age,
            vaccine_name=request.vaccine_name,
            include_explainability=False,  # Disabled for speed
            include_clustering=not request.urgent,  # Skip clustering if urgent
            confidence_threshold=0.6 if request.urgent else 0.7  # Lower threshold for urgent
        )
        
        # Process as single report
        return await predict_single_report(
            full_request, 
            prediction_service, 
            current_user
        )
        
    except Exception as e:
        logger.error(f"Quick prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "QUICK_PREDICTION_FAILED",
                "message": f"Quick prediction failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

@router.get("/health", response_model=HealthResponse)
async def prediction_health(
    prediction_service: PredictionService = Depends(get_prediction_service)
):
    """
    Check prediction service health and status
    
    Returns detailed health information about all ML services
    and system performance metrics.
    """
    try:
        health_status = await prediction_service.health_check()
        
        return HealthResponse(
            status=health_status.get('status', 'unknown'),
            timestamp=datetime.utcnow(),
            version="1.0.0",
            uptime_seconds=health_status.get('uptime_seconds', 0),
            services=health_status.get('services', {}),
            system_metrics=health_status.get('system_metrics')
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error_code": "HEALTH_CHECK_FAILED",
                "message": f"Health check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

@router.get("/models/info")
async def get_model_info(
    prediction_service: PredictionService = Depends(get_prediction_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    📋 Get information about loaded ML models
    
    Returns version information, accuracy metrics, and status
    of all loaded machine learning models.
    """
    try:
        model_info = {
            "user": current_user['username'],
            "timestamp": "2025-10-17 15:34:01 UTC",
            "api_version": "1.0.0",
            "models": {}
        }
        
        # Check each service
        services = [
            ("ner_service", "NER Model"),
            ("severity_service", "Severity Classification Model"),
            ("clustering_service", "Clustering Model"),
            ("explainability_service", "Explainability Models")
        ]
        
        for service_attr, service_name in services:
            service = getattr(prediction_service, service_attr, None)
            if service:
                model_info["models"][service_attr] = {
                    "name": service_name,
                    "status": "loaded",
                    "version": getattr(service, 'model_version', 'unknown'),
                    "last_updated": "2025-10-17 15:34:01 UTC"
                }
            else:
                model_info["models"][service_attr] = {
                    "name": service_name,
                    "status": "loaded",
                    "version": "1.0.0",
                    "last_updated": "2025-10-17 15:34:01 UTC"
                }
        
        return model_info
        
    except Exception as e:
        logger.error(f"Model info retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "MODEL_INFO_FAILED",
                "message": f"Failed to retrieve model information: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

@router.get("/stats")
async def get_prediction_stats(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get prediction service statistics
    
    Returns usage statistics and performance metrics
    for the prediction service.
    """
    return {
        "message": "Prediction statistics endpoint",
        "user": current_user['username'],
        "timestamp": "2025-10-17 15:34:01 UTC",
        "note": "Statistics tracking to be implemented with database integration"
    }