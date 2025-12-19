# ADEGuard: AI-Driven Adverse Drug Event Detection System

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Models](#models)
- [Data Pipeline](#data-pipeline)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Citation](#citation)

---

## 🎯 Overview

**ADEGuard** is an advanced AI-powered system designed to detect and classify **Adverse Drug Events (ADEs)** from pharmaceutical safety reports. Built on a microservices architecture, it combines multiple machine learning models for comprehensive analysis including Named Entity Recognition (NER), severity classification, clustering, and explainability.

The system processes VAERS (Vaccine Adverse Event Reporting System) data and other ADE reports to:
- Extract clinical entities (drugs, symptoms, conditions)
- Classify severity levels
- Cluster similar events
- Provide interpretable explanations for predictions

---

## ✨ Features

### Core Capabilities
- 🔍 **Named Entity Recognition (NER)** - Extract drug names, symptoms, and adverse events using BioBERT
- 📊 **Severity Classification** - Automatically classify ADE severity levels
- 🎯 **Event Clustering** - Group similar adverse events using advanced clustering algorithms
- 💡 **Explainability** - Understand model predictions with SHAP and LIME
- ⚡ **Batch Processing** - Process multiple reports simultaneously
- 📈 **Interactive Dashboard** - Real-time visualization and analytics

### Technical Features
- FastAPI REST API with OpenAPI documentation
- Streamlit web dashboard for easy interaction
- Docker containerization for deployment
- Comprehensive logging and monitoring
- Unit tests and integration tests
- Weak supervision for label generation
- ML pipeline optimization

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  ADEGuard System Architecture                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Streamlit Dashboard (Frontend)               │   │
│  │  - Interactive UI for data visualization             │   │
│  │  - Report submission and management                  │   │
│  │  - Analytics and insights                            │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │ HTTP/REST                             │
│                       ▼                                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │      FastAPI Backend (Microservices Layer)           │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │  NER Service        (Entity Extraction)      │   │   │
│  │  │  - BioBERT Model                             │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │  Severity Service   (Risk Assessment)        │   │   │
│  │  │  - Classification Model                      │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │  Clustering Service (Event Grouping)         │   │   │
│  │  │  - HDBSCAN Algorithm                         │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │  Explainability Service (Interpretability)   │   │   │
│  │  │  - SHAP & LIME Explainers                    │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                       │                                       │
│  ┌────────────────────▼──────────────────────────────────┐  │
│  │           Data Storage & Processing                   │  │
│  │  - VAERS Datasets (CSV)                              │  │
│  │  - Embeddings (NumPy files)                           │  │
│  │  - Model Checkpoints (SafeTensors)                    │  │
│  │  - Results & Analytics                               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: Minimum 8GB (16GB recommended for GPU support)
- **Disk**: At least 20GB free space (models and datasets)
- **GPU** (Optional): NVIDIA GPU with CUDA 11.8+ for faster inference

### Required Software
```
✓ Python 3.8+
✓ Git
✓ Git LFS (for large files)
✓ Docker & Docker Compose (for containerized deployment)
```

---

## 🚀 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/adeguard-project.git
cd adeguard-project
```

### Step 2: Pull Large Files (if using Git LFS)

```bash
git lfs pull
```

### Step 3: Setup Backend API

**Option A: Using Virtual Environment (Recommended)**

```cmd
cd adeguard_backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Option B: Using Docker**

```cmd
cd adeguard_backend
docker build -t adeguard-backend .
docker run -p 8000:8000 adeguard-backend
```

### Step 4: Setup Streamlit Dashboard

```cmd
cd adeguard_streamlit_dashboard

# Create virtual environment
python -m venv streamlit_venv

# Activate virtual environment
# On Windows:
streamlit_venv\Scripts\activate
# On macOS/Linux:
source streamlit_venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Verify Installation

```cmd
# Check Python packages
pip list

# Verify model files exist
dir /s /B saved_models\
dir /s /B biobert_ner_adeguard\
```

---

## ⚡ Quick Start

### Run Backend & Frontend Locally

**Terminal 1: Start FastAPI Backend**

```cmd
cd adeguard_backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Terminal 2: Start Streamlit Dashboard**

```cmd
cd adeguard_streamlit_dashboard
streamlit_venv\Scripts\activate
streamlit run app.py
```

Expected output:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Access Applications

| Application | URL | Purpose |
|-------------|-----|---------|
| Streamlit Dashboard | http://localhost:8501 | Web UI for interacting with the system |
| FastAPI Swagger UI | http://localhost:8000/docs | API documentation and testing |
| FastAPI ReDoc | http://localhost:8000/redoc | Alternative API documentation |
| Health Check | http://localhost:8000/health | System status verification |

---

## 📁 Project Structure

```
adeguard-project/
│
├── adeguard_backend/              # FastAPI backend microservices
│   ├── app/
│   │   ├── api/v1/                # REST API endpoints
│   │   │   └── endpoints/
│   │   │       ├── predict.py      # Prediction endpoints
│   │   │       ├── reports.py      # Report management
│   │   │       ├── auth.py         # Authentication
│   │   │       └── admin.py        # Admin operations
│   │   ├── core/
│   │   │   ├── config.py           # Configuration settings
│   │   │   └── security.py         # Security utilities
│   │   ├── models/
│   │   │   ├── request_models.py   # Request schemas
│   │   │   └── response_models.py  # Response schemas
│   │   ├── services/
│   │   │   ├── ner_service.py          # NER service
│   │   │   ├── severity_service.py     # Severity classification
│   │   │   ├── clustering_service.py   # Event clustering
│   │   │   └── explainability_service.py # Model explanation
│   │   ├── utils/
│   │   │   ├── logging_utils.py    # Logging configuration
│   │   │   ├── validators.py       # Input validation
│   │   │   └── helpers.py          # Utility functions
│   │   └── main.py                 # FastAPI app entry point
│   ├── saved_models/               # Trained models
│   │   ├── ner_model/
│   │   ├── severity_model/
│   │   ├── clustering_model/
│   │   └── explainability_models/
│   ├── logs/                       # Application logs
│   ├── tests/
│   │   ├── test_api.py             # API tests
│   │   ├── test_main.py            # Main app tests
│   │   └── test_services.py        # Service unit tests
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Docker image definition
│   └── docker-compose.yml          # Docker Compose config
│
├── adeguard_streamlit_dashboard/   # Streamlit web UI
│   ├── app.py                      # Main dashboard app
│   ├── utils/
│   │   ├── api_client.py           # API communication
│   │   ├── formatters.py           # Data formatting
│   │   └── visualizers.py          # Plotting utilities
│   ├── pages/                      # Multi-page sections
│   ├── assets/                     # Static assets
│   ├── components/                 # Reusable components
│   ├── requirements.txt            # Dashboard dependencies
│   └── streamlit_venv/             # Virtual environment
│
├── biobert_ner_adeguard/           # BioBERT NER model
│   ├── model.safetensors           # Model weights
│   ├── config.json                 # Model configuration
│   ├── tokenizer.json              # Tokenizer
│   ├── vocab.txt                   # Vocabulary
│   └── checkpoint-*/               # Training checkpoints
│
├── saved_models/                   # Serialized ML models
│   ├── ner_model/
│   ├── severity_model/
│   ├── clustering_model/
│   └── explainability_models/
│
├── clustering_embeddings/          # Embedding vectors
│   ├── combined_embeddings.npy
│   ├── text_embeddings.npy
│   └── embedding_metadata.json
│
├── datasets/                       # Data files
│   ├── 2025VAERSDATA.csv
│   ├── 2025VAERSSYMPTOMS.csv
│   ├── 2025VAERSVAX.csv
│   └── vaers_integrated.csv
│
├── weak_labels_output_py311/       # Weak supervision outputs
│   ├── training_data.json
│   └── weak_labels_complete.json
│
├── clustering_results/             # Clustering analysis
│   ├── clustered_data.csv
│   ├── clustering_report.json
│   └── interactive_clusters.html
│
├── explainability_results/         # Model explanations
│   ├── clinical_insights_report.json
│   └── explainability_final_comprehensive_report.json
│
├── severity_classification_results/# Classification results
│   ├── classification_report.json
│   └── saved_models/
│
├── .gitignore                      # Git ignore patterns
├── .gitattributes                  # Git LFS tracking
├── .env.example                    # Environment template
├── SETUP.md                        # Setup instructions
├── README.md                       # This file
└── GITHUB_UPLOAD_GUIDE.md          # GitHub upload guide
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
# ========== Backend API Configuration ==========
API_HOST=localhost
API_PORT=8000
DEBUG=True

# ========== Database ==========
DATABASE_URL=sqlite:///./test.db

# ========== Model Paths ==========
NER_MODEL_PATH=./biobert_ner_adeguard
CLUSTERING_MODEL_PATH=./saved_models/clustering_model
SEVERITY_MODEL_PATH=./saved_models/severity_model
EXPLAINABILITY_MODEL_PATH=./saved_models/explainability_models

# ========== Logging ==========
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# ========== Security ==========
SECRET_KEY=your_secret_key_here
API_KEY=your_api_key_here
```

### Backend Configuration (`adeguard_backend/app/core/config.py`)

Key settings:
- `HOST`: API server host (default: `0.0.0.0`)
- `PORT`: API server port (default: `8000`)
- `DEBUG`: Enable debug mode (default: `True`)
- `MODEL_PATHS`: Paths to model files
- `BATCH_SIZE`: Inference batch size
- `MAX_SEQ_LENGTH`: Maximum sequence length for NER

---

## 📖 Usage Guide

### Via Streamlit Dashboard

1. **Start the Dashboard** (see Quick Start section)
2. **Upload/Select Data**:
   - Upload VAERS CSV file
   - Or select pre-loaded dataset
3. **Run Analysis**:
   - Click "Run ADE Detection"
   - Monitor progress in real-time
4. **View Results**:
   - Extracted entities (drugs, symptoms)
   - Severity classification
   - Event clustering visualization
   - Model explanations

### Via REST API

#### Single Report Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict/single \
  -H "Content-Type: application/json" \
  -d '{
    "symptom_text": "Patient experienced severe rash and fever after vaccination",
    "patient_age": 35,
    "include_explainability": true,
    "include_clustering": true
  }'
```

#### Batch Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "reports": [
      {"symptom_text": "...", "patient_age": 25},
      {"symptom_text": "...", "patient_age": 45}
    ]
  }'
```

#### Get Model Information

```bash
curl -X GET http://localhost:8000/api/v1/predict/models/info \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### System Health Check

```bash
curl http://localhost:8000/health
```

---

## 🤖 Models

### 1. NER Service (Named Entity Recognition)

**Model**: BioBERT (Fine-tuned on biomedical data)

**Capabilities**:
- Extract drug names
- Identify adverse symptoms
- Recognize medical conditions
- Extract dosage information

**Input**: Clinical text (symptom description)
**Output**: List of extracted entities with types and confidence scores

**Files**:
- `biobert_ner_adeguard/model.safetensors` - Model weights
- `biobert_ner_adeguard/config.json` - Configuration
- `biobert_ner_adeguard/tokenizer.json` - Tokenizer

### 2. Severity Classification Service

**Model**: Multi-class classifier (trained on VAERS data)

**Severity Levels**:
- `Low`: Minor symptoms, no hospitalization
- `Medium`: Significant symptoms, may require medical attention
- `High`: Serious symptoms, hospitalization required
- `Critical`: Life-threatening, requires emergency intervention

**Input**: Extracted entities + text
**Output**: Severity level + confidence score

### 3. Clustering Service

**Algorithm**: HDBSCAN (Hierarchical Density-Based Clustering)

**Purpose**:
- Group similar adverse events
- Identify event patterns
- Detect signal clusters

**Input**: Event embeddings (from sentence-transformers)
**Output**: Cluster assignments + cluster labels

### 4. Explainability Service

**Methods**:
- SHAP (SHapley Additive exPlanations) - Feature importance
- LIME (Local Interpretable Model-agnostic Explanations) - Local explanations

**Purpose**:
- Explain model predictions
- Show feature importance
- Provide clinical insights

**Output**: Explanation visualizations + feature contributions

---

## 📊 Data Pipeline

### Input Data Format

**VAERS CSV Structure**:
```csv
VAERS_ID,AGE_YRS,SEX,SYMPTOM_TEXT,ONSET_DATE,VAX_NAME
123456,35,F,"Nausea, rash, fatigue",2025-01-15,COVID-19 mRNA
```

### Processing Steps

```
1. Data Loading
   ↓
2. Data Validation
   ↓
3. Text Preprocessing
   - Lowercasing
   - Tokenization
   - Cleaning
   ↓
4. Entity Extraction (NER)
   ↓
5. Severity Classification
   ↓
6. Embedding Generation
   ↓
7. Event Clustering
   ↓
8. Explainability Analysis
   ↓
9. Report Generation
```

### Weak Supervision

The project includes weak supervision setup for generating training labels:
- Rule-based label functions
- Pattern matching
- Heuristic-based labeling
- Snorkel integration for label aggregation

See `03_weak_supervision_setup_py311_Version2.ipynb` for details.

---

## 🔍 Notebooks

The project includes comprehensive Jupyter notebooks for analysis and training:

| Notebook | Purpose |
|----------|---------|
| `01_Data_collection_preprocessing.ipynb` | Data loading, cleaning, and preprocessing |
| `03_weak_supervision_setup_py311_Version2.ipynb` | Weak label generation |
| `04_biobert_ner_setup_py311.ipynb` | NER model training and evaluation |
| `05_clustering.ipynb` | Event clustering analysis |
| `06_severity_classification.ipynb` | Severity model training |
| `07_explainibility.ipynb` | Explainability analysis |

---

## 🧪 Testing

### Run Unit Tests

```cmd
cd adeguard_backend

# Run all tests
pytest -v

# Run specific test file
pytest tests/test_services.py -v

# Run with coverage
pytest --cov=app tests/
```

### Test Files

- `tests/test_api.py` - API endpoint tests
- `tests/test_main.py` - Application tests
- `tests/test_services.py` - Service unit tests

### Manual Testing

```cmd
# Test NER endpoint
curl -X POST http://localhost:8000/api/v1/predict/single \
  -H "Content-Type: application/json" \
  -d '{"symptom_text": "Patient had fever and chills"}'

# Test health check
curl http://localhost:8000/health

# Check model info
curl http://localhost:8000/api/v1/predict/models/info
```

---

## 🐳 Docker Deployment

### Build Docker Image

```cmd
cd adeguard_backend
docker build -t adeguard-backend:latest .
```

### Run with Docker Compose

```cmd
cd adeguard_backend
docker-compose up -d
```

This starts:
- FastAPI backend on port 8000
- All required services
- Volumes for logs and models

### Docker Commands

```cmd
# View running containers
docker-compose ps

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose build --no-cache
docker-compose up -d
```

---

## 🔧 Troubleshooting

### Issue 1: ModuleNotFoundError: No module named 'app'

**Solution**:
```cmd
cd adeguard_backend
uvicorn app.main:app --reload
```

Ensure you run from the `adeguard_backend` directory, not the `app` subdirectory.

### Issue 2: Models not loaded ("not_loaded" status)

**Solution**:
Check backend logs for errors:
```cmd
tail -f adeguard_backend/logs/app.log
```

Common causes:
- Model files missing or corrupted
- Insufficient disk space
- Out of memory

### Issue 3: Connection refused (Cannot connect to backend)

**Solution**:
1. Verify backend is running:
```cmd
curl http://localhost:8000/health
```

2. Check if port 8000 is in use:
```cmd
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000
```

3. Use different port:
```cmd
uvicorn app.main:app --port 8080
```

### Issue 4: Out of Memory errors

**Solution**:
- Reduce batch size in config
- Use CPU instead of GPU
- Process fewer records at once
- Increase available RAM/VRAM

### Issue 5: Streamlit cache issues

**Solution**:
```cmd
streamlit cache clear
streamlit run app.py
```

### Issue 6: Slow inference

**Solution**:
- Use GPU acceleration (if available)
- Reduce sequence length
- Increase batch size
- Check system resources (CPU, RAM)

### Getting Help

Check logs:
```cmd
# Backend logs
cat adeguard_backend/logs/app.log

# Streamlit logs (in terminal where streamlit is running)
```

---

## 📈 Performance Metrics

### Expected Performance

| Component | Latency | Throughput |
|-----------|---------|-----------|
| NER (single) | 100-200ms | ~100 reports/min |
| Severity Classification | 50-100ms | ~200 reports/min |
| Clustering | 500ms-2s | ~30-60 reports/min |
| Full Pipeline | 2-5s | ~10-30 reports/min |

*Metrics vary based on hardware, model size, and batch size*

### System Requirements by Workload

| Workload | CPU | RAM | GPU |
|----------|-----|-----|-----|
| Development | 2+ cores | 8GB | Optional |
| Small deployment | 4 cores | 16GB | Optional |
| Production | 8+ cores | 32GB | Recommended |

---

## 🤝 Contributing

### Development Setup

```bash
# Clone and setup
git clone <repository>
cd adeguard-project

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
pytest tests/

# Commit with descriptive message
git commit -m "feat: description of changes"

# Push and create pull request
git push origin feature/your-feature-name
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints in functions
- Write docstrings for all functions
- Add unit tests for new features

### Commit Messages

Format: `type: description`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat: add LIME explainability support
fix: resolve NER tokenizer issue
docs: update API documentation
```

---

## 📝 Citation

If you use ADEGuard in your research, please cite:

```bibtex
@software{adeguard2025,
  title={ADEGuard: AI-Driven Adverse Drug Event Detection System},
  author={Ghanashyam},
  year={2025},
  url={https://github.com/yourusername/adeguard-project}
}
```

---

## 📜 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📞 Support

### Documentation
- 📖 [SETUP.md](SETUP.md) - Detailed setup instructions
- 📖 [GITHUB_UPLOAD_GUIDE.md](GITHUB_UPLOAD_GUIDE.md) - GitHub deployment guide
- 📖 [API Docs](http://localhost:8000/docs) - Interactive API documentation

### Contact
- **Author**: Ghanashyam
- **Email**: ghanashyam9348@example.com
- **Issues**: Create an issue in the GitHub repository

---

## 🙏 Acknowledgments

- BioBERT team for the pre-trained NER model
- VAERS program for providing safety data
- Streamlit team for the amazing dashboard framework
- FastAPI team for the modern web framework
- SHAP and LIME teams for explainability methods

---

## 🗺️ Roadmap

### v1.1 (Planned)
- [ ] Multi-language support
- [ ] Enhanced visualization dashboard
- [ ] API rate limiting
- [ ] Advanced caching mechanisms

### v1.2 (Planned)
- [ ] Real-time alert system
- [ ] Email notifications
- [ ] Advanced analytics
- [ ] Data export features

### v2.0 (Future)
- [ ] Federated learning support
- [ ] Graph-based clustering
- [ ] Transfer learning for domain adaptation
- [ ] Mobile application

---

**Last Updated**: December 19, 2025

**Version**: 1.0.0

**Status**: ✅ Active & Production-Ready

---

**Built with ❤️ for healthcare safety**
