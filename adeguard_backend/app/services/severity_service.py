# ADEGuard Backend API - Severity Service
# Current Date and Time (UTC): 2025-10-17 14:37:50
# Current User's Login: ghanashyam9348

import logging
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import numpy as np
import joblib

class SeverityService:
    """Severity Classification Service"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.vectorizer = None
        self.scaler = None
        self.model_version = "severity-classifier-v1.0"
        self.severity_labels = ['mild', 'moderate', 'severe', 'life_threatening']
        
    async def load_model(self):
        """Load severity classification model"""
        try:
            self.logger.info("Loading severity classification model...")
            
            model_path = Path("../severity_classification_results/saved_models")
            
            if model_path.exists():
                # Try to load trained model components
                model_files = {
                    'model': model_path / 'best_model.joblib',
                    'vectorizer': model_path / 'tfidf_vectorizer.joblib', 
                    'scaler': model_path / 'scaler.joblib'
                }
                
                for component, file_path in model_files.items():
                    if file_path.exists():
                        setattr(self, component, joblib.load(file_path))
                        self.logger.info(f"Loaded {component} from {file_path}")
            
            # Fallback: Create simple rule-based classifier
            if not self.model:
                self.logger.info("Creating rule-based severity classifier")
                self._create_rule_based_classifier()
            
            self.logger.info("✅ Severity model loaded successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load severity model: {e}")
            self._create_rule_based_classifier()
    
    async def classify_severity(self, text: str, entities: List[Dict], patient_age: Optional[int] = None) -> Dict[str, Any]:
        """Classify severity of ADE report"""
        
        try:
            # Rule-based prediction as primary method
            predicted_class, confidence, severity_probs = self._rule_based_prediction(text, entities)
            predicted_severity = self.severity_labels[predicted_class]
            
            return {
                'predicted_severity': predicted_severity,
                'confidence': float(confidence),
                'severity_probabilities': severity_probs,
                'method': 'rule_based'
            }
            
        except Exception as e:
            self.logger.error(f"Severity classification failed: {e}")
            return {
                'predicted_severity': 'unknown',
                'confidence': 0.0,
                'severity_probabilities': {},
                'error': str(e)
            }
    
    def _rule_based_prediction(self, text: str, entities: List[Dict]) -> Tuple[int, float, Dict[str, float]]:
        """Rule-based severity prediction"""
        
        text_lower = text.lower()
        
        # Life-threatening indicators
        if any(word in text_lower for word in ['death', 'die', 'life-threatening', 'anaphylaxis', 'cardiac arrest']):
            return 3, 0.9, {'mild': 0.0, 'moderate': 0.05, 'severe': 0.05, 'life_threatening': 0.9}
        
        # Severe indicators
        if any(word in text_lower for word in ['hospitalized', 'emergency', 'severe', 'intensive care']):
            return 2, 0.8, {'mild': 0.05, 'moderate': 0.15, 'severe': 0.8, 'life_threatening': 0.0}
        
        # Moderate indicators
        if any(word in text_lower for word in ['fever', 'high temperature', 'vomiting', 'difficulty breathing']):
            return 1, 0.7, {'mild': 0.2, 'moderate': 0.7, 'severe': 0.1, 'life_threatening': 0.0}
        
        # Default to mild
        return 0, 0.6, {'mild': 0.6, 'moderate': 0.3, 'severe': 0.1, 'life_threatening': 0.0}
    
    def _create_rule_based_classifier(self):
        """Create a simple rule-based classifier"""
        class RuleBasedClassifier:
            def predict(self, X):
                return [1]  # Default to moderate
        
        self.model = RuleBasedClassifier()
    
    async def health_check(self) -> Dict[str, Any]:
        """Severity service health check"""
        if not self.model:
            return {'status': 'not_loaded'}
        
        try:
            test_result = await self.classify_severity(
                "patient had severe fever after vaccination", 
                [{'label': 'ADE', 'text': 'fever'}], 
                35
            )
            return {
                'status': 'healthy',
                'model_version': self.model_version,
                'test_prediction': test_result['predicted_severity']
            }
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    async def cleanup(self):
        """Cleanup severity service resources"""
        self.model = None
        self.vectorizer = None
        self.scaler = None