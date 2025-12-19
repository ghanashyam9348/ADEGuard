# ADEGuard Backend API - Project Structure Setup
# Current Date and Time (UTC): 2025-10-17 14:21:01
# Current User's Login: ghanashyam9348
# Step 8.1: Setting up the FastAPI project structure

import os
from pathlib import Path

def create_backend_structure():
    """Create the FastAPI backend project structure"""
    
    print(f"🚀 ADEGuard Step 8.1: Backend API Project Structure Setup")
    print(f"👤 User: ghanashyam9348")
    print(f"🕐 Time: 2025-10-17 14:21:01 UTC")
    print(f"📁 Creating FastAPI backend structure...")
    
    # Define project structure
    project_structure = {
        'adeguard_backend': {
            'app': {
                '__init__.py': '',
                'main.py': '# FastAPI main application',
                'config.py': '# Configuration settings',
                'dependencies.py': '# Dependency injection',
                'api': {
                    '__init__.py': '',
                    'v1': {
                        '__init__.py': '',
                        'endpoints': {
                            '__init__.py': '',
                            'predict.py': '# Prediction endpoints',
                            'reports.py': '# Report management',
                            'auth.py': '# Authentication',
                            'admin.py': '# Admin functions'
                        },
                        'api.py': '# API router setup'
                    }
                },
                'core': {
                    '__init__.py': '',
                    'security.py': '# Security functions',
                    'config.py': '# Core configuration'
                },
                'models': {
                    '__init__.py': '',
                    'ml_models.py': '# ML model wrappers',
                    'request_models.py': '# Pydantic request models',
                    'response_models.py': '# Pydantic response models',
                    'database_models.py': '# Database models'
                },
                'services': {
                    '__init__.py': '',
                    'prediction_service.py': '# Prediction logic',
                    'ner_service.py': '# NER processing',
                    'clustering_service.py': '# Clustering service',
                    'severity_service.py': '# Severity classification',
                    'explainability_service.py': '# SHAP/LIME service'
                },
                'utils': {
                    '__init__.py': '',
                    'text_processing.py': '# Text utilities',
                    'model_utils.py': '# Model utilities',
                    'logging_utils.py': '# Logging setup'
                }
            },
            'tests': {
                '__init__.py': '',
                'test_main.py': '# Main tests',
                'test_api.py': '# API tests',
                'test_services.py': '# Service tests'
            },
            'saved_models': {
                'ner_model': {},
                'severity_model': {},
                'clustering_model': {},
                'explainability_models': {}
            },
            'requirements.txt': '# Python dependencies',
            'Dockerfile': '# Docker configuration',
            'docker-compose.yml': '# Docker Compose setup',
            '.env': '# Environment variables',
            'README.md': '# Project documentation'
        }
    }
    
    def create_directory_structure(base_path, structure):
        """Recursively create directory structure"""
        for name, content in structure.items():
            current_path = base_path / name
            
            if isinstance(content, dict):
                # It's a directory
                current_path.mkdir(parents=True, exist_ok=True)
                print(f"   📁 Created directory: {current_path}")
                create_directory_structure(current_path, content)
            else:
                # It's a file
                current_path.parent.mkdir(parents=True, exist_ok=True)
                if not current_path.exists():
                    with open(current_path, 'w') as f:
                        f.write(content)
                    print(f"   📄 Created file: {current_path}")
    
    # Create the structure
    base_path = Path.cwd() / 'adeguard_backend'
    create_directory_structure(Path.cwd(), project_structure)
    
    print(f"\n✅ FastAPI backend structure created successfully!")
    print(f"📁 Base directory: {base_path}")
    
    return base_path

# Create the project structure
backend_path = create_backend_structure()

print(f"\n📋 Next Steps:")
print(f"   1. cd adeguard_backend")
print(f"   2. Create virtual environment: python -m venv venv")
print(f"   3. Activate virtual environment: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
print(f"   4. Install dependencies: pip install -r requirements.txt")
print(f"   5. Run the FastAPI server: uvicorn app.main:app --reload")