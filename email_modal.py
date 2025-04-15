import streamlit as st

def email_modal(email_content: str):
    # CSS for the modal
    st.markdown("""
        <style>
        .modal-backdrop {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .modal-container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            width: 90%;
            max-width: 800px;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
            padding: 24px;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid #eee;
        }
        .modal-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #1a1a1a;
            margin: 0;
        }
        .modal-body {
            flex-grow: 1;
            overflow-y: auto;
            margin-bottom: 20px;
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 16px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.5;
            white-space: pre-wrap;
        }
        .modal-footer {
            display: flex;
            justify-content: flex-end;
            gap: 12px;
            padding-top: 16px;
            border-top: 1px solid #eee;
        }
        .copy-success {
            color: #28a745;
            font-size: 0.9em;
            margin-right: auto;
            display: flex;
            align-items: center;
        }
        .copy-success::before {
            content: '✓';
            margin-right: 6px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

    # Initialize session state for copy success message
    if 'show_copy_success' not in st.session_state:
        st.session_state.show_copy_success = False

    # Modal structure
    st.markdown("""
        <div class="modal-container">
            <div class="modal-header">
                <h3 class="modal-title">Stakeholder Email Template</h3>
            </div>
            <div class="modal-body">
                {}
            </div>
            <div class="modal-footer">
                {}
            </div>
        </div>
    """.format(
        email_content,
        '<div class="copy-success">Email content copied to clipboard!</div>' if st.session_state.show_copy_success else ''
    ), unsafe_allow_html=True)

    # Buttons
    col1, col2, col3 = st.columns([6, 2, 2])
    with col2:
        if st.button("Copy", type="primary", key="copy_button"):
            st.session_state.show_copy_success = True
            st.rerun()
    with col3:
        if st.button("Close", type="secondary", key="close_button"):
            return True
    
    return False

def generate_email_content(risk_insights) -> str:
    """
    Generate email content based on current risk insights
    """
    current_date = datetime.now().strftime("%B %d, %Y")
    
    email_template = f"""
Subject: Supply Chain Risk Assessment and Mitigation Update - {current_date}

Dear Stakeholders,

I hope this email finds you well. I am writing to provide a critical update on our current supply chain risk landscape and the mitigation measures we are implementing.

KEY RISK AREAS:
"""

    # Add each risk insight to the email
    for risk in risk_insights:
        email_template += f"""
{risk['event']}
- Impact Level: {risk['impact_level']}
- Affected Area: {risk['affected_entity']}
- Mitigation Plan: {risk['recommendation']}
"""

    email_template += """

NEXT STEPS:
1. Review the attached mitigation plans for each risk area
2. Schedule follow-up meetings with respective regional teams
3. Update contingency plans based on current risk assessments

Please review these updates and share any concerns or additional insights you may have. We will be holding a detailed review meeting next week to discuss these matters further.

Best regards,
Supply Chain Risk Management Team
"""
    
    return email_template 