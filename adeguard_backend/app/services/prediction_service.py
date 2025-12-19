# ADEGuard Backend API - Main Prediction Service
# Current Date and Time (UTC): 2025-10-17 14:37:50
# Current User's Login: ghanashyam9348

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any
import uuid
from datetime import datetime

class PredictionService:
    """Main prediction service coordinating all ML components"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
        self.model_versions = {}
        self.initialization_time = None
        
        # Import services (will be created next)
        self.ner_service = None
        self.clustering_service = None
        self.severity_service = None
        self.explainability_service = None
        
        print(f"🔧 PredictionService initializing...")
        print(f"👤 User: ghanashyam9348")
        print(f"🕐 Time: 2025-10-17 14:37:50 UTC")
    
    async def load_models(self):
        """Load all ML models and services"""
        try:
            start_time = time.time()
            self.logger.info("Loading ADEGuard ML models...")
            
            # Import and initialize services
            from .ner_service import NERService
            from .severity_service import SeverityService
            from .clustering_service import ClusteringService
            from .explainability_service import ExplainabilityService
            
            self.ner_service = NERService()
            self.severity_service = SeverityService()
            self.clustering_service = ClusteringService()
            self.explainability_service = ExplainabilityService()
            
            # Load models in parallel
            await asyncio.gather(
                self.ner_service.load_model(),
                self.severity_service.load_model(),
                self.clustering_service.load_model(),
                self.explainability_service.load_models()
            )
            
            self.is_initialized = True
            self.initialization_time = time.time() - start_time
            
            self.logger.info(f"✅ All models loaded successfully in {self.initialization_time:.2f}s")
            
        except Exception as e:
            self.logger.error(f"❌ Model loading failed: {e}")
            raise
    
    async def predict(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main prediction pipeline"""
        
        if not self.is_initialized:
            raise RuntimeError("Services not initialized")
        
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        try:
            # Extract text
            symptom_text = request_data.get('symptom_text', '')
            patient_age = request_data.get('patient_age')
            include_explainability = request_data.get('include_explainability', True)
            include_clustering = request_data.get('include_clustering', True)
            
            results = {
                'request_id': request_id,
                'timestamp': datetime.utcnow(),
                'processing_steps': {}
            }
            
            # Step 1: NER - Extract entities
            step_start = time.time()
            ner_results = await self.ner_service.extract_entities(symptom_text)
            results['extracted_entities'] = ner_results['entities']
            results['processing_steps']['ner_time'] = time.time() - step_start
            
            # Step 2: Severity Classification
            step_start = time.time()
            severity_results = await self.severity_service.classify_severity(
                symptom_text, ner_results['entities'], patient_age
            )
            results['severity_analysis'] = severity_results
            results['processing_steps']['severity_time'] = time.time() - step_start
            
            # Step 3: Clustering Analysis (optional)
            if include_clustering:
                step_start = time.time()
                cluster_results = await self.clustering_service.analyze_cluster(
                    symptom_text, ner_results['entities'], patient_age
                )
                results['cluster_analysis'] = cluster_results
                results['processing_steps']['clustering_time'] = time.time() - step_start
            
            # Step 4: Explainability (optional)
            if include_explainability:
                step_start = time.time()
                explainability_results = await self.explainability_service.generate_explanations(
                    symptom_text, severity_results, ner_results['entities']
                )
                results['explainability'] = explainability_results
                results['processing_steps']['explainability_time'] = time.time() - step_start
            
            # Generate summary and alerts
            results['summary'] = self._generate_summary(results)
            results['alerts'] = self._generate_alerts(results)
            results['recommendations'] = self._generate_recommendations(results)
            
            # Processing metrics
            total_time = time.time() - start_time
            results['processing_metrics'] = {
                'total_processing_time': total_time,
                'ner_processing_time': results['processing_steps'].get('ner_time', 0),
                'severity_classification_time': results['processing_steps'].get('severity_time', 0),
                'clustering_time': results['processing_steps'].get('clustering_time', 0),
                'explainability_time': results['processing_steps'].get('explainability_time', 0)
            }
            
            self.logger.info(f"✅ Prediction completed for {request_id} in {total_time:.2f}s")
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Prediction failed for {request_id}: {e}")
            raise
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate high-level summary"""
        severity = results.get('severity_analysis', {}).get('predicted_severity', 'unknown')
        entities = results.get('extracted_entities', [])
        
        ade_count = len([e for e in entities if e.get('label') == 'ADE'])
        drug_count = len([e for e in entities if e.get('label') == 'DRUG'])
        
        return {
            'severity_level': severity,
            'ade_entities_found': ade_count,
            'drug_entities_found': drug_count,
            'total_entities': len(entities),
            'requires_attention': severity in ['severe', 'life_threatening']
        }
    
    def _generate_alerts(self, results: Dict[str, Any]) -> List[str]:
        """Generate critical alerts"""
        alerts = []
        severity = results.get('severity_analysis', {}).get('predicted_severity', 'unknown')
        confidence = results.get('severity_analysis', {}).get('confidence', 0)
        
        if severity == 'life_threatening':
            alerts.append("🚨 CRITICAL: Life-threatening ADE detected - Immediate medical attention required")
        elif severity == 'severe':
            alerts.append("⚠️ SEVERE: Severe ADE detected - Medical evaluation recommended")
        
        if confidence > 0.9:
            alerts.append(f"🎯 HIGH CONFIDENCE: Prediction confidence {confidence:.1%}")
        elif confidence < 0.6:
            alerts.append(f"⚠️ LOW CONFIDENCE: Prediction confidence {confidence:.1%} - Manual review recommended")
        
        return alerts
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate clinical recommendations"""
        recommendations = []
        severity = results.get('severity_analysis', {}).get('predicted_severity', 'unknown')
        
        if severity in ['severe', 'life_threatening']:
            recommendations.extend([
                "Immediately assess patient vital signs",
                "Consider discontinuation of suspected medication",
                "Document all symptoms and timeline thoroughly",
                "Report to pharmacovigilance system"
            ])
        elif severity == 'moderate':
            recommendations.extend([
                "Monitor patient closely for symptom progression",
                "Consider dose adjustment or alternative medication",
                "Schedule follow-up within 24-48 hours"
            ])
        else:
            recommendations.extend([
                "Continue monitoring for symptom changes",
                "Patient education on symptom recognition",
                "Document for future reference"
            ])
        
        return recommendations
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for all services"""
        status = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'initialization_time': self.initialization_time,
            'services': {}
        }
        
        if not self.is_initialized:
            status['status'] = 'not_initialized'
            return status
        
        return status
    
    async def cleanup(self):
        """Cleanup resources"""
        self.logger.info("🔄 Cleaning up PredictionService...")