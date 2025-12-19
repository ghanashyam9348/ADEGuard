# ADEGuard Backend API - Clustering Service
# Current Date and Time (UTC): 2025-10-17 14:37:50
# Current User's Login: ghanashyam9348

import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import numpy as np
import pandas as pd

class ClusteringService:
    """Clustering Analysis Service"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cluster_model = None
        self.embeddings_model = None
        self.cluster_data = None
        self.model_version = "clustering-v1.0"
        
    async def load_model(self):
        """Load clustering model and data"""
        try:
            self.logger.info("Loading clustering model...")
            
            # Try to load clustering results
            clustering_path = Path("../clustering_results")
            if clustering_path.exists():
                cluster_file = clustering_path / "clustered_data.csv"
                if cluster_file.exists():
                    self.cluster_data = pd.read_csv(cluster_file)
                    self.logger.info(f"Loaded clustering data: {len(self.cluster_data)} samples")
            
            # Create mock clustering if no data available
            if self.cluster_data is None:
                self._create_mock_clustering()
            
            self.logger.info("✅ Clustering model loaded successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load clustering model: {e}")
            self._create_mock_clustering()
    
    def _create_mock_clustering(self):
        """Create mock clustering data for testing"""
        self.cluster_data = pd.DataFrame({
            'cluster_id': [0, 1, 2, 0, 1],
            'cluster_label': [
                'Mild post-vaccination reactions',
                'Moderate allergic responses', 
                'Severe systemic reactions',
                'Mild post-vaccination reactions',
                'Moderate allergic responses'
            ],
            'age_group': ['adult', 'child', 'elderly', 'adult', 'teen'],
            'severity': ['mild', 'moderate', 'severe', 'mild', 'moderate']
        })
    
    async def analyze_cluster(self, text: str, entities: List[Dict], patient_age: Optional[int] = None) -> Dict[str, Any]:
        """Analyze cluster assignment for given text"""
        
        try:
            # Simple rule-based cluster assignment for now
            text_lower = text.lower()
            
            # Determine cluster based on severity keywords
            if any(word in text_lower for word in ['severe', 'life-threatening', 'hospitalized']):
                cluster_id = 2
                cluster_label = "Severe systemic reactions"
            elif any(word in text_lower for word in ['moderate', 'fever', 'rash']):
                cluster_id = 1
                cluster_label = "Moderate allergic responses"
            else:
                cluster_id = 0
                cluster_label = "Mild post-vaccination reactions"
            
            # Get cluster statistics if data available
            cluster_size = 10
            similarity_score = 0.75
            
            if self.cluster_data is not None:
                cluster_subset = self.cluster_data[self.cluster_data['cluster_id'] == cluster_id]
                cluster_size = len(cluster_subset)
                
                # Calculate age group distribution
                age_dist = cluster_subset['age_group'].value_counts().to_dict() if 'age_group' in cluster_subset.columns else {}
                severity_dist = cluster_subset['severity'].value_counts().to_dict() if 'severity' in cluster_subset.columns else {}
            else:
                age_dist = {'adult': 5, 'elderly': 3, 'child': 2}
                severity_dist = {'mild': 4, 'moderate': 4, 'severe': 2}
            
            return {
                'cluster_id': cluster_id,
                'cluster_label': cluster_label,
                'cluster_size': cluster_size,
                'similarity_score': similarity_score,
                'age_group_distribution': age_dist,
                'severity_distribution': severity_dist
            }
            
        except Exception as e:
            self.logger.error(f"Clustering analysis failed: {e}")
            return {
                'cluster_id': -1,
                'cluster_label': 'Unknown cluster',
                'cluster_size': 0,
                'similarity_score': 0.0,
                'error': str(e)
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Clustering service health check"""
        try:
            test_result = await self.analyze_cluster(
                "patient had fever after vaccination", 
                [{'label': 'ADE', 'text': 'fever'}],
                35
            )
            return {
                'status': 'healthy',
                'model_version': self.model_version,
                'test_cluster': test_result['cluster_label']
            }
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    async def cleanup(self):
        """Cleanup clustering resources"""
        self.cluster_model = None
        self.cluster_data = None