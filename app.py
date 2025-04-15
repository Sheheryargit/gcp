import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from event_card import event_card
from risk_card import risk_card
from chat_ui import chat_ui
from email_modal import email_modal, generate_email_content

# Page configuration
st.set_page_config(
    page_title="Supply Chain Risk Intelligence Dashboard",
    page_icon="��",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    .stTitle {
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: #1a1a1a !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Subtitle styling */
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #eee;
    }
    
    /* Stats container */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #0066cc;
    }
    
    /* Footer styling */
    .footer {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Button styling */
    .stButton button {
        font-weight: 500 !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-1px) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for modal
if 'show_email_modal' not in st.session_state:
    st.session_state.show_email_modal = False

# Title and subtitle
st.title("Supply Chain Risk Intelligence Dashboard")
st.markdown('<p class="subtitle">Powered by Agentic AI | Real-Time Global Disruption Monitoring</p>', unsafe_allow_html=True)

# Quick stats
st.markdown("""
    <div class="stats-container">
        <div style="flex: 1; text-align: center;">
            <div style="font-size: 2rem; font-weight: 600; color: #dc3545;">3</div>
            <div style="color: #666;">High Risk Events</div>
        </div>
        <div style="flex: 1; text-align: center;">
            <div style="font-size: 2rem; font-weight: 600; color: #ffc107;">5</div>
            <div style="color: #666;">Active Alerts</div>
        </div>
        <div style="flex: 1; text-align: center;">
            <div style="font-size: 2rem; font-weight: 600; color: #28a745;">89%</div>
            <div style="color: #666;">Route Efficiency</div>
        </div>
        <div style="flex: 1; text-align: center;">
            <div style="font-size: 2rem; font-weight: 600; color: #0066cc;">24</div>
            <div style="color: #666;">Monitored Routes</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Create three columns for the layout
left_col, middle_col, right_col = st.columns(3)

# Sample data for events
events = [
    {
        "title": "Port Congestion in Shanghai",
        "summary": "Major delays reported at Shanghai port with container dwell times increasing by 50%. Impacting vessel schedules across Asia-Pacific routes.",
        "tags": ["Logistics", "Asia", "High Risk"],
        "date": "2024-04-06 • 2h ago"
    },
    {
        "title": "New Trade Regulations in EU",
        "summary": "European Union announces stricter environmental regulations for maritime shipping, affecting cargo vessels entering EU ports.",
        "tags": ["Regulatory", "Europe", "Medium Risk"],
        "date": "2024-04-06 • 4h ago"
    },
    {
        "title": "Labor Strike in Rotterdam",
        "summary": "Dock workers union announces 48-hour strike at Port of Rotterdam. Expected to cause significant delays in cargo handling.",
        "tags": ["Labor", "Europe", "High Risk"],
        "date": "2024-04-06 • 6h ago"
    }
]

# Sample data for risk insights
risk_insights = [
    {
        "event": "Supply Chain Delay Risk",
        "affected_entity": "Asia-Pacific Shipping Routes",
        "impact_level": "High",
        "recommendation": "Activate alternative shipping routes through Singapore. Consider air freight for high-priority cargo."
    },
    {
        "event": "Cost Impact Analysis",
        "affected_entity": "European Operations",
        "impact_level": "Medium",
        "recommendation": "Review and adjust Q2 logistics budget. Consider long-term contracts to stabilize costs."
    },
    {
        "event": "Inventory Risk Assessment",
        "affected_entity": "Regional Distribution Centers",
        "impact_level": "Low",
        "recommendation": "Maintain current inventory levels. Review safety stock calculations in Q3."
    }
]

# Left column - Event Feed
with left_col:
    st.markdown('<div class="section-header">Latest Global Events</div>', unsafe_allow_html=True)
    for event in events:
        event_card(
            title=event["title"],
            summary=event["summary"],
            tags=event["tags"],
            date=event["date"]
        )

# Middle column - Risk Insights
with middle_col:
    st.markdown('<div class="section-header">Supply Chain Risk Insights</div>', unsafe_allow_html=True)
    for risk in risk_insights:
        risk_card(
            event=risk["event"],
            affected_entity=risk["affected_entity"],
            impact_level=risk["impact_level"],
            recommendation=risk["recommendation"]
        )
    
    if st.button("Generate Stakeholder Email", type="primary"):
        st.session_state.show_email_modal = True

# Right column - Chatbot
with right_col:
    st.markdown('<div class="section-header">Ask Agentic AI</div>', unsafe_allow_html=True)
    chat_ui()

# Show email modal if button was clicked
if st.session_state.show_email_modal:
    email_content = generate_email_content(risk_insights)
    should_close = email_modal(email_content)
    if should_close:
        st.session_state.show_email_modal = False
        st.rerun()

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown(f"Last updated: {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
st.markdown('</div>', unsafe_allow_html=True) 