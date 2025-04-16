import streamlit as st
import time

def chat_ui():
    # CSS for the chat interface
    st.markdown("""
        <style>
        .chat-container {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .message-container {
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding-right: 10px;
        }
        .message {
            margin: 8px 0;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user-message {
            background-color: #007bff;
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }
        .assistant-message {
            background-color: #f0f2f6;
            color: #1a1a1a;
            margin-right: auto;
            border-bottom-left-radius: 5px;
        }
        .message-time {
            font-size: 0.7em;
            color: #666;
            margin-top: 4px;
            text-align: right;
        }
        .typing-indicator {
            display: flex;
            padding: 10px 15px;
            background-color: #f0f2f6;
            border-radius: 15px;
            margin: 8px 0;
            width: fit-content;
        }
        .typing-dot {
            width: 8px;
            height: 8px;
            margin: 0 2px;
            background-color: #666;
            border-radius: 50%;
            animation: typing 1s infinite;
            display: inline-block;
        }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-5px); }
        }
        </style>
        """, unsafe_allow_html=True)

    # Initialize session state for messages if not exists
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'is_typing' not in st.session_state:
        st.session_state.is_typing = False

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Messages container
    st.markdown('<div class="message-container">', unsafe_allow_html=True)
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Show typing indicator if AI is "thinking"
    if st.session_state.is_typing:
        st.markdown("""
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close message-container

    # Input area
    with st.container():
        col1, col2 = st.columns([8, 2])
        with col1:
            prompt = st.chat_input("Ask about supply chain risks...", key="chat_input", label_visibility="collapsed")
        with col2:
            send_button = st.button("Send", type="primary", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close chat-container

    # Handle send button click
    if send_button and prompt:
        # Add user message to chat history
        current_time = time.strftime("%H:%M")
        st.session_state.messages.append({"role": "user", "content": prompt, "time": current_time})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Simulate AI thinking
        st.session_state.is_typing = True
        st.rerun()

    # Simulate AI response after typing indicator
    if st.session_state.is_typing:
        # Simulate processing delay
        time.sleep(1)
        
        # Generate AI response
        current_time = time.strftime("%H:%M")
        response = generate_ai_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response, "time": current_time})
        
        # Reset typing indicator
        st.session_state.is_typing = False
        st.rerun()

def generate_ai_response(user_input: str) -> str:
    """
    Simulate AI response generation. This will be replaced with actual RAG model later.
    """
    responses = {
        "risk": "Based on current data, the main supply chain risks are port congestion in Asia (High), labor strikes in Europe (Medium), and weather conditions in the Mediterranean (Low).",
        "delay": "Current average delay times are: Asia routes: 3-5 days, European routes: 1-2 days, Americas: On schedule.",
        "cost": "Freight rates have increased by 15% in Q1 2024. Main factors: fuel costs, capacity constraints, and new environmental regulations.",
        "inventory": "Current inventory levels are within optimal range. Buffer stock is maintained at 3 weeks for critical components.",
    }
    
    # Simple keyword matching
    for keyword, response in responses.items():
        if keyword in user_input.lower():
            return response
    
    return "I understand your query about supply chain operations. Could you please provide more specific details about what information you need?" 