import streamlit as st
import pandas as pd
from datetime import datetime
from event_card import event_card
from risk_card import risk_card
from chat_ui import chat_ui
from email_modal import email_modal, generate_email_content
from news_api import fetch_supply_chain_news

# Page config
st.set_page_config(
    page_title="Supply Chain Risk Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    /* Main container styling */
    .main-container {
        padding: 2rem;
        background: #f8f9fa;
    }
    
    /* Header styling */
    .header {
        margin-bottom: 2rem;
    }
    
    /* Title styling */
    .title {
        color: #1a1a1a;
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle styling */
    .subtitle {
        color: #666;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Stats container */
    .stats-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    
    /* Section title styling */
    .section-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    /* Footer styling */
    .footer {
        margin-top: 2rem;
        color: #666;
        font-size: 0.9rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for email modal
if 'show_email_modal' not in st.session_state:
    st.session_state.show_email_modal = False

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown('<div class="header">', unsafe_allow_html=True)
st.markdown('<h1 class="title">Supply Chain Risk Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Real-time monitoring and analysis of global supply chain risks</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Stats Container
st.markdown('<div class="stats-container">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Active Risks", "12", "+2")
with col2:
    st.metric("Risk Score", "6.8", "-0.5")
with col3:
    st.metric("Affected Regions", "8", "+1")
with col4:
    st.metric("Critical Events", "3", "+1")
st.markdown('</div>', unsafe_allow_html=True)

# Main content columns
col1, col2, col3 = st.columns([1, 1, 1])

# Global Events Column
with col1:
    st.markdown('<h2 class="section-title">Global Events</h2>', unsafe_allow_html=True)
    news_items = fetch_supply_chain_news(days_back=2)
    for news in news_items:
        event_card(
            title=news['title'],
            summary=news['description'],
            tags=news['relevance_tags'],
            date=news['published_at'],
            source=news['source'],
            url=news['url']
        )

# Risk Insights Column
with col2:
    st.markdown('<h2 class="section-title">Supply Chain Risk Insights</h2>', unsafe_allow_html=True)
    
    # Generate risk insights based on news items
    for news in news_items:
        # Use the relevance tags to determine risk level
        risk_level = "High" if "Risk" in news['relevance_tags'] else \
                    "Medium" if any(tag in ["Transportation", "Manufacturing"] for tag in news['relevance_tags']) else \
                    "Low"
        
        # Extract affected entity from relevance tags and source
        affected_categories = [tag for tag in news['relevance_tags'] if tag != "Risk"]
        affected_entity = f"{news['source']} ({', '.join(affected_categories)})" if affected_categories else news['source']
        
        # Generate recommendation based on risk level and tags
        if risk_level == "High":
            recommendation = f"Immediate action required: Monitor {', '.join(affected_categories).lower() if affected_categories else 'situation'} and develop contingency plans"
        elif risk_level == "Medium":
            recommendation = f"Monitor {', '.join(affected_categories).lower() if affected_categories else 'situation'} closely and prepare alternative solutions"
        else:
            recommendation = "Regular monitoring advised, no immediate action required"
        
        # Create risk card
        risk_card(
            event=news['title'],
            affected_entity=affected_entity,
            impact_level=risk_level,
            recommendation=recommendation
        )

    # Email generation button
    if st.button("Generate Stakeholder Email", type="primary"):
        st.session_state.show_email_modal = True

# Chat Interface Column
with col3:
    st.markdown('<h2 class="section-title">Risk Analysis Chat</h2>', unsafe_allow_html=True)
    chat_ui()

# Email Modal
if st.session_state.show_email_modal:
    risk_insights = [
        f"Risk: {news['title']} - Impact Level: {risk_level}"
        for news in news_items
    ]
    email_content = generate_email_content(risk_insights)
    email_modal(email_content)

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown(f'Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) 