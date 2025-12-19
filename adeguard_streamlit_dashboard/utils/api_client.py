# ADEGuard Dashboard - API Client with Network Support
# Current Date and Time (UTC): 2025-10-18 20:12:33
# Current User's Login: ghanashyam9348

import requests
import streamlit as st
from typing import Dict, Any, Optional
import logging
import socket

class ADEGuardAPIClient:
    """API client for ADEGuard backend communication with network support"""
    
    def __init__(self, base_url: str = None):
        # Auto-detect API URL
        if base_url is None:
            base_url = self._detect_api_url()
        
        self.base_url = base_url.rstrip('/')
        self.auth_token = "test_token_ghanashyam9348"
        self.timeout = 30
        self.headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'ADEGuard-Dashboard/1.0.0'
        }
    
    def _detect_api_url(self) -> str:
        """Auto-detect FastAPI backend URL"""
        possible_urls = [
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            f"http://{self._get_local_ip()}:8000",
            "http://0.0.0.0:8000"
        ]
        
        for url in possible_urls:
            try:
                response = requests.get(f"{url}/health", timeout=5)
                if response.status_code == 200:
                    print(f"✅ FastAPI backend detected at: {url}")
                    return url
            except:
                continue
        
        print("⚠️ FastAPI backend not detected, using default: http://localhost:8000")
        return "http://localhost:8000"
    
    def _get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except:
            return "localhost"
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Make HTTP request to backend API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, headers=self.headers, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            return {
                "error": "Cannot connect to backend API", 
                "details": f"Backend server may be down at {self.base_url}",
                "suggestion": "Ensure FastAPI server is running with: uvicorn app.main:app --host 0.0.0.0 --port 8000"
            }
        except requests.exceptions.Timeout:
            return {"error": "Request timeout", "details": "API request took too long"}
        except requests.exceptions.HTTPError as e:
            return {"error": f"HTTP {e.response.status_code}", "details": str(e)}
        except Exception as e:
            return {"error": "Unexpected error", "details": str(e)}
    
    # Keep all existing methods...
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        return self._make_request('GET', '/health')
    
    def predict_single_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit single ADE report prediction"""
        return self._make_request('POST', '/api/v1/predict/single', data=report_data)
    
    def predict_batch_reports(self, batch_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit batch ADE report prediction"""
        return self._make_request('POST', '/api/v1/predict/batch', data=batch_data)
    
    def get_api_info(self) -> Dict[str, Any]:
        """Get API information"""
        return self._make_request('GET', '/api/v1/info')
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return self._make_request('GET', '/api/v1/predict/models/info')
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        return self._make_request('GET', '/api/v1/admin/system/status')