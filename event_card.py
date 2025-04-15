import streamlit as st

def event_card(title: str, summary: str, tags: list[str], date: str):
    # CSS for the card
    st.markdown("""
        <style>
        .event-card {
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border: 1px solid #eee;
        }
        .event-title {
            color: #1a1a1a;
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .event-summary {
            color: #4a4a4a;
            font-size: 0.9em;
            margin-bottom: 12px;
            line-height: 1.4;
        }
        .event-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 10px;
        }
        .event-tag {
            background-color: #f0f2f6;
            color: #444;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            display: inline-block;
        }
        .event-date {
            color: #666;
            font-size: 0.8em;
            text-align: right;
        }
        </style>
        """, unsafe_allow_html=True)

    # Render the card using HTML
    st.markdown(f"""
        <div class="event-card">
            <div class="event-title">{title}</div>
            <div class="event-summary">{summary}</div>
            <div class="event-tags">
                {''.join([f'<span class="event-tag">{tag}</span>' for tag in tags])}
            </div>
            <div class="event-date">{date}</div>
        </div>
    """, unsafe_allow_html=True) 