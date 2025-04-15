import streamlit as st

def risk_card(event: str, affected_entity: str, impact_level: str, recommendation: str):
    # Validate impact level
    if impact_level not in ['Low', 'Medium', 'High']:
        raise ValueError("impact_level must be one of: Low, Medium, High")

    # CSS for the card
    st.markdown("""
        <style>
        .risk-card {
            background-color: white;
            border-radius: 6px;
            padding: 20px;
            margin: 12px 0;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            border-left: 4px solid #ddd;
        }
        .risk-card.High {
            border-left-color: #dc3545;
        }
        .risk-card.Medium {
            border-left-color: #ffc107;
        }
        .risk-card.Low {
            border-left-color: #28a745;
        }
        .risk-event {
            color: #2c3e50;
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .risk-entity {
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
        }
        .risk-entity::before {
            content: '🏢';
            margin-right: 6px;
        }
        .impact-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 500;
            margin-bottom: 12px;
        }
        .impact-badge.High {
            background-color: #fde8e8;
            color: #dc3545;
        }
        .impact-badge.Medium {
            background-color: #fff8e6;
            color: #b7791f;
        }
        .impact-badge.Low {
            background-color: #e6f6e6;
            color: #28a745;
        }
        .risk-recommendation {
            background-color: #f8f9fa;
            border-radius: 4px;
            padding: 12px;
            color: #495057;
            font-size: 0.9em;
            line-height: 1.5;
        }
        .risk-recommendation::before {
            content: '💡';
            margin-right: 6px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Render the card using HTML
    st.markdown(f"""
        <div class="risk-card {impact_level}">
            <div class="risk-event">{event}</div>
            <div class="risk-entity">{affected_entity}</div>
            <div class="impact-badge {impact_level}">
                {impact_level} Impact
            </div>
            <div class="risk-recommendation">
                {recommendation}
            </div>
        </div>
    """, unsafe_allow_html=True) 