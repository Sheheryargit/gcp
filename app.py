import streamlit as st
from event_card import event_card
from risk_card import risk_card
from chat_ui import chat_ui
from email_modal import email_modal, generate_email_content
from news_api import fetch_supply_chain_news
from datetime import datetime

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

# Left column - Event Feed
with left_col:
    st.markdown('<div class="section-header">Latest Global Events</div>', unsafe_allow_html=True)
    # Fetch real news articles
    news_articles = fetch_supply_chain_news(days_back=2)
    for article in news_articles:
        event_card(
            title=article['title'],
            summary=article['description'],
            tags=article['relevance_tags'],
            date=article['published_at'],
            source=article['source'],
            url=article['url']
        )

# Middle column - Risk Insights
with middle_col:
    st.markdown('<div class="section-header">Supply Chain Risk Insights</div>', unsafe_allow_html=True)
    risk_insights = [
        {
            "event": "Port Congestion in Asia",
            "affected_entity": "Maritime Shipping Routes",
            "impact_level": "High",
            "recommendation": "Consider alternative routes through less congested ports or air freight options for critical shipments."
        },
        {
            "event": "Semiconductor Shortage",
            "affected_entity": "Electronics Manufacturing",
            "impact_level": "Medium",
            "recommendation": "Diversify supplier base and increase safety stock levels for critical components."
        },
        {
            "event": "Weather Disruption",
            "affected_entity": "Ground Transportation",
            "impact_level": "Low",
            "recommendation": "Monitor weather patterns and prepare alternative delivery routes."
        }
    ]
    
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
    email_modal(generate_email_content(risk_insights))

# Footer
st.markdown(f"""
    <div class="footer">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
""", unsafe_allow_html=True) 