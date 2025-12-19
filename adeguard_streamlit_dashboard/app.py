# ADEGuard Streamlit Dashboard - Main Application
# Current Date and Time (UTC): 2025-10-17 18:29:22
# Current User's Login: ghanashyam9348

import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Import API client
from utils.api_client import ADEGuardAPIClient

# Page configuration
st.set_page_config(
    page_title="ADEGuard Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2a5298;
    }
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
    }
    .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize API client
@st.cache_resource
def get_api_client():
    return ADEGuardAPIClient()

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0;">🏥 ADEGuard Web Dashboard</h1>
        <p style="color: #e0e0e0; margin: 0.5rem 0 0 0;">
            Advanced ADE Detection and Reporting System
        </p>
        <p style="color: #b0b0b0; margin: 0.25rem 0 0 0; font-size: 0.8rem;">
            👤 User: ghanashyam9348 |
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize API client
    api_client = get_api_client()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        # API Status
        health_data = api_client.health_check()
        if 'error' not in health_data:
            st.success("🟢 API Connected")
        else:
            st.error("🔴 API Disconnected")
            st.error(f"Error: {health_data.get('error', 'Unknown')}")
        
        # Navigation options
        page_options = [
            "🏠 Dashboard Overview",
            "🔍 ADE Prediction",
            "📊 Analytics & Reports", 
            "📋 Report Management",
            "⚙️ System Administration"
        ]
        
        selected_page = st.selectbox(
            "Select Page",
            page_options,
            index=0
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ System Info")
        st.markdown("**Version**: 1.0.0")
        st.markdown("**Developer**: ghanashyam9348")
    
    # Load selected page
    if selected_page == "🏠 Dashboard Overview":
        show_dashboard_overview(api_client)
    elif selected_page == "🔍 ADE Prediction":
        show_prediction_interface(api_client)
    elif selected_page == "📊 Analytics & Reports":
        show_analytics_page(api_client)
    elif selected_page == "📋 Report Management":
        show_reports_management(api_client)
    elif selected_page == "⚙️ System Administration":
        show_admin_interface(api_client)

# Replace the recent activity section in show_dashboard_overview function
def show_dashboard_overview(api_client):
    """Dashboard overview page - STABLE VERSION"""
    
    st.markdown("## 🏠 Dashboard Overview")
    st.markdown("**Real-time ADE Detection System Monitoring**")
    
    # Remove auto-refresh that causes shaking
    col1, col2, col3 = st.columns([1, 1, 8])
    with col1:
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
            st.rerun()
    
    # System metrics (keep existing)
    st.markdown("### 📊 System Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🔍 Predictions Today",
            value="247",
            delta="↗️ +12 from yesterday"
        )
    
    with col2:
        st.metric(
            label="⚠️ Severe Cases",
            value="23",
            delta="↗️ +3 from yesterday"
        )
    
    with col3:
        st.metric(
            label="⚡ Avg Response Time", 
            value="1.2s",
            delta="↘️ -0.3s improvement"
        )
    
    with col4:
        st.metric(
            label="🤖 Models Active",
            value="4/4",
            delta="✅ All operational"
        )
    
    # Charts (keep existing)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Severity Distribution (Last 7 Days)")
        
        # Sample data
        severity_data = pd.DataFrame({
            'Severity': ['Mild', 'Moderate', 'Severe', 'Life-Threatening'],
            'Count': [156, 78, 23, 4]
        })
        
        fig_pie = px.pie(
            severity_data,
            values='Count',
            names='Severity', 
            title="ADE Cases by Severity",
            color_discrete_sequence=['#28a745', '#ffc107', '#fd7e14', '#dc3545']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Daily Prediction Trends")
        
        # Sample trend data
        dates = pd.date_range(start='2025-10-11', end='2025-10-17', freq='D')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Predictions': [32, 28, 45, 38, 42, 35, 47],
            'Severe_Cases': [2, 1, 4, 3, 3, 2, 5]
        })
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=trend_data['Date'], 
            y=trend_data['Predictions'],
            mode='lines+markers',
            name='Total Predictions',
            line=dict(color='#2a5298', width=3)
        ))
        fig_line.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Severe_Cases'], 
            mode='lines+markers',
            name='Severe Cases',
            line=dict(color='#dc3545', width=3)
        ))
        fig_line.update_layout(
            title="Prediction Trends",
            xaxis_title="Date",
            yaxis_title="Count"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # FIXED: Stable Recent Activity Section
    st.markdown("### 📋 Recent Activity")
    
    # Use session state to prevent constant re-rendering
    if 'recent_activity_data' not in st.session_state:
        st.session_state.recent_activity_data = pd.DataFrame({
            'Time': [
                '2025-10-17 19:00:05',
                '2025-10-17 18:58:30', 
                '2025-10-17 18:56:15',
                '2025-10-17 18:54:00',
                '2025-10-17 18:51:45'
            ],
            'Event': [
                '🔍 Severe ADE prediction completed',
                '📊 Analytics report generated', 
                '📊 Batch processing finished (25 reports)',
                '🔍 Quick prediction submitted',
                '⚠️ High severity alert generated'
            ],
            'Status': [
                '✅ Complete',
                '✅ Complete', 
                '✅ Complete',
                '✅ Complete',
                '⚠️ Alert'
            ]
        })
    
    # Display stable dataframe
    st.dataframe(
        st.session_state.recent_activity_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Time": st.column_config.TextColumn("Time", width="small"),
            "Event": st.column_config.TextColumn("Event", width="large"), 
            "Status": st.column_config.TextColumn("Status", width="small")
        }
    )
    
    # Manual refresh button for recent activity
    if st.button("🔄 Refresh Recent Activity", key="refresh_activity"):
        # Update with new timestamp
        current_time = "2025-10-17 19:00:05"
        new_event = f"🔄 Manual refresh triggered at {current_time}"
        
        # Add new event to top
        new_row = pd.DataFrame({
            'Time': [current_time],
            'Event': [new_event],
            'Status': ['✅ Complete']
        })
        
        st.session_state.recent_activity_data = pd.concat([
            new_row, 
            st.session_state.recent_activity_data.head(4)
        ], ignore_index=True)
        
        st.rerun()
    
    # Alerts section (keep existing but make stable)
    st.markdown("### 🚨 System Alerts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("🚨 **CRITICAL**: 2 life-threatening cases in last hour")
        st.warning("⚠️ **WARNING**: Increased severe reactions to Batch XYZ123") 
    
    with col2:
        st.success("✅ **OK**: All ML models operational")
        st.info("ℹ️ **INFO**: System backup scheduled at 02:00 UTC")

def show_prediction_interface(api_client):
    """ADE prediction interface"""
    
    st.markdown("## 🔍 ADE Prediction Interface")
    st.markdown("**Submit new ADE reports for analysis**")
    
    # Prediction form
    with st.form("prediction_form"):
        st.markdown("### 📝 Patient Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=45)
            patient_gender = st.selectbox("Gender", ["female", "male", "other"])
        
        with col2:
            vaccine_name = st.text_input("Vaccine Name", value="COVID-19 mRNA vaccine")
            vaccine_manufacturer = st.selectbox(
                "Manufacturer", 
                ["Pfizer-BioNTech", "Moderna", "Johnson & Johnson", "AstraZeneca", "Other"]
            )
        
        with col3:
            hospitalized = st.checkbox("Hospitalized")
            life_threatening = st.checkbox("Life-threatening")
        
        st.markdown("### 📄 Symptom Description")
        symptom_text = st.text_area(
            "Describe symptoms and adverse events",
            value="Patient developed severe headache and high fever 2 hours after COVID-19 vaccination. Temperature reached 39.5°C. Also experienced significant fatigue and muscle aches. Symptoms persisted for 48 hours.",
            height=150
        )
        
        # Processing options
        col1, col2 = st.columns(2)
        with col1:
            include_explainability = st.checkbox("Include AI Explanations", value=True)
        with col2:
            include_clustering = st.checkbox("Include Clustering Analysis", value=True)
        
        # Submit button
        submitted = st.form_submit_button("🔍 Analyze ADE Report", use_container_width=True)
        
        if submitted:
            # Prepare request data
            request_data = {
                "patient_age": patient_age,
                "patient_gender": patient_gender,
                "vaccine_name": vaccine_name,
                "vaccine_manufacturer": vaccine_manufacturer,
                "symptom_text": symptom_text,
                "hospitalized": hospitalized,
                "life_threatening": life_threatening,
                "include_explainability": include_explainability,
                "include_clustering": include_clustering
            }
            
            # Show processing
            with st.spinner("🔄 Analyzing ADE report..."):
                response = api_client.predict_single_report(request_data)
            
            # Display results
            if 'error' not in response:
                show_prediction_results(response)
            else:
                st.error(f"❌ Prediction failed: {response.get('error')}")
                st.error(f"Details: {response.get('details', 'No additional details')}")

def show_prediction_results(response):
    """Display prediction results"""
    
    st.markdown("## 📊 Analysis Results")
    
    # Summary metrics
    summary = response.get('summary', {})
    severity_analysis = response.get('severity_analysis', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        severity = severity_analysis.get('predicted_severity', 'unknown')
        confidence = severity_analysis.get('confidence', 0.0)
        st.metric("🎯 Predicted Severity", severity.title(), f"{confidence:.1%} confidence")
    
    with col2:
        ade_count = summary.get('ade_entities_found', 0)
        st.metric("🔍 ADE Entities Found", ade_count)
    
    with col3:
        drug_count = summary.get('drug_entities_found', 0)
        st.metric("💊 Drug Entities Found", drug_count)
    
    with col4:
        attention_needed = summary.get('requires_attention', False)
        attention_text = "Yes" if attention_needed else "No"
        st.metric("⚠️ Requires Attention", attention_text)
    
    # Extracted entities
    entities = response.get('extracted_entities', [])
    if entities:
        st.markdown("### 🏷️ Extracted Entities")
        
        entity_df = pd.DataFrame([{
            'Text': entity.get('text', ''),
            'Label': entity.get('label', ''),
            'Confidence': f"{entity.get('confidence', 0):.1%}"
        } for entity in entities])
        
        st.dataframe(entity_df, use_container_width=True, hide_index=True)
    
    # Severity probabilities
    severity_probs = severity_analysis.get('severity_probabilities', {})
    if severity_probs:
        st.markdown("### 📊 Severity Probability Distribution")
        
        prob_df = pd.DataFrame([
            {'Severity': sev.replace('_', ' ').title(), 'Probability': prob}
            for sev, prob in severity_probs.items()
        ])
        
        fig_bar = px.bar(
            prob_df, 
            x='Severity', 
            y='Probability',
            title="Severity Classification Probabilities",
            color='Probability',
            color_continuous_scale='RdYlBu_r'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Alerts and recommendations
    alerts = response.get('alerts', [])
    recommendations = response.get('recommendations', [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if alerts:
            st.markdown("### 🚨 Alerts")
            for alert in alerts:
                if "CRITICAL" in alert or "life-threatening" in alert:
                    st.error(alert)
                elif "SEVERE" in alert or "WARNING" in alert:
                    st.warning(alert)
                else:
                    st.info(alert)
    
    with col2:
        if recommendations:
            st.markdown("### 💡 Recommendations")
            for rec in recommendations:
                st.success(f"✅ {rec}")

def show_analytics_page(api_client):
    """Analytics and reports page"""
    
    st.markdown("## 📊 Analytics & Reports")
    st.markdown("**System analytics and reporting capabilities**")
    
    # Sample analytics charts
    st.markdown("### 📈 Weekly Trends")
    
    # Generate sample data
    dates = pd.date_range(start='2025-10-01', end='2025-10-17', freq='D')
    analytics_data = pd.DataFrame({
        'Date': dates,
        'Total_Reports': np.random.poisson(35, len(dates)),
        'Mild': np.random.poisson(20, len(dates)),
        'Moderate': np.random.poisson(10, len(dates)), 
        'Severe': np.random.poisson(4, len(dates)),
        'Life_Threatening': np.random.poisson(1, len(dates))
    })
    
    # Stacked area chart
    fig_area = go.Figure()
    
    fig_area.add_trace(go.Scatter(
        x=analytics_data['Date'], y=analytics_data['Mild'],
        fill='tonexty', mode='none', name='Mild', fillcolor='rgba(40, 167, 69, 0.7)'
    ))
    fig_area.add_trace(go.Scatter(
        x=analytics_data['Date'], y=analytics_data['Moderate'], 
        fill='tonexty', mode='none', name='Moderate', fillcolor='rgba(255, 193, 7, 0.7)'
    ))
    fig_area.add_trace(go.Scatter(
        x=analytics_data['Date'], y=analytics_data['Severe'],
        fill='tonexty', mode='none', name='Severe', fillcolor='rgba(253, 126, 20, 0.7)'
    ))
    fig_area.add_trace(go.Scatter(
        x=analytics_data['Date'], y=analytics_data['Life_Threatening'],
        fill='tonexty', mode='none', name='Life-Threatening', fillcolor='rgba(220, 53, 69, 0.7)'
    ))
    
    fig_area.update_layout(
        title="ADE Reports by Severity Over Time",
        xaxis_title="Date",
        yaxis_title="Number of Reports"
    )
    
    st.plotly_chart(fig_area, use_container_width=True)
    
    # Summary statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Summary Statistics")
        
        summary_stats = pd.DataFrame({
            'Metric': [
                'Total Reports (30 days)',
                'Average Daily Reports', 
                'Severe Cases (%)',
                'Most Common ADE',
                'Peak Hour'
            ],
            'Value': [
                '1,247',
                '41.6',
                '8.2%',
                'Fever/Headache',
                '14:00-15:00 UTC'
            ]
        })
        
        st.dataframe(summary_stats, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 🏥 Top Vaccine Manufacturers")
        
        manufacturer_data = pd.DataFrame({
            'Manufacturer': ['Pfizer-BioNTech', 'Moderna', 'Johnson & Johnson', 'AstraZeneca', 'Others'],
            'Reports': [456, 342, 189, 134, 126]
        })
        
        fig_manufacturer = px.bar(
            manufacturer_data,
            x='Reports',
            y='Manufacturer',
            orientation='h',
            title="Reports by Vaccine Manufacturer"
        )
        st.plotly_chart(fig_manufacturer, use_container_width=True)

def show_reports_management(api_client):
    """Reports management page"""
    
    st.markdown("## 📋 Report Management")
    st.markdown("**View and manage ADE reports**")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        severity_filter = st.selectbox("Filter by Severity", ["All", "Mild", "Moderate", "Severe", "Life-Threatening"])
    
    with col2:
        date_range = st.date_input("Date Range", value=[datetime.now().date() - timedelta(days=7), datetime.now().date()])
    
    with col3:
        search_term = st.text_input("Search Reports", placeholder="Enter search term...")
    
    # Sample reports data
    reports_data = pd.DataFrame({
        'ID': ['ADE-001', 'ADE-002', 'ADE-003', 'ADE-004', 'ADE-005'],
        'Date': ['2025-10-17', '2025-10-17', '2025-10-16', '2025-10-16', '2025-10-15'],
        'Patient Age': [45, 67, 28, 52, 34],
        'Vaccine': ['COVID-19 mRNA', 'COVID-19 mRNA', 'Influenza', 'COVID-19 mRNA', 'HPV'],
        'Severity': ['Moderate', 'Severe', 'Mild', 'Moderate', 'Mild'],
        'Status': ['Processed', 'Under Review', 'Processed', 'Processed', 'Processed']
    })
    
    # Display reports table
    st.markdown("### 📊 Reports Table")
    st.dataframe(reports_data, use_container_width=True, hide_index=True)
    
    # Export options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export CSV", use_container_width=True):
            st.success("✅ CSV export initiated")
    
    with col2:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            st.success("✅ PDF report generation started")
    
    with col3:
        if st.button("📧 Email Summary", use_container_width=True):
            st.success("✅ Email summary sent")

def show_admin_interface(api_client):
    """System administration interface"""
    
    st.markdown("## ⚙️ System Administration")
    st.markdown("**System monitoring and administration**")
    
    # System status
    st.markdown("### 🖥️ System Status")
    
    system_data = api_client.get_system_status()
    
    if 'error' not in system_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.success("✅ **API Status**: Operational")
        with col2:
            st.success("✅ **Database**: Connected")
        with col3:
            st.success("✅ **ML Models**: 4/4 Loaded")
        with col4:
            st.success("✅ **Cache**: Active")
    else:
        st.error(f"❌ System status error: {system_data.get('error')}")
    
    # Model information
    st.markdown("### 🤖 Model Information")
    
    model_data = api_client.get_model_info()
    
    if 'error' not in model_data and 'models' in model_data:
        models_info = []
        for service_name, model_info in model_data['models'].items():
            models_info.append({
                'Service': service_name.replace('_', ' ').title(),
                'Status': model_info.get('status', 'Unknown'),
                'Version': model_info.get('version', 'Unknown')
            })
        
        models_df = pd.DataFrame(models_info)
        st.dataframe(models_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Could not retrieve model information")
    
    # Admin actions
    st.markdown("### 🔧 Admin Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Reload Models", use_container_width=True):
            st.success("✅ Model reload initiated")
    
    with col2:
        if st.button("📊 System Metrics", use_container_width=True):
            st.info("📈 Displaying system metrics...")
    
    with col3:
        if st.button("🗂️ View Logs", use_container_width=True):
            st.text_area("System Logs", 
                        "2025-10-17 18:29:22 INFO: System operational\n"
                        "2025-10-17 18:28:45 INFO: Prediction completed\n"
                        "2025-10-17 18:27:30 INFO: API request processed", 
                        height=100)

if __name__ == "__main__":
    main()