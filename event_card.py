import streamlit as st
from datetime import datetime

def event_card(title: str, summary: str, tags: list, date: str, source: str = None, url: str = None):
    """
    Display a card showing a supply chain event.
    
    Args:
        title (str): Event title
        summary (str): Event description
        tags (list): List of tags/categories
        date (str): ISO format date string
        source (str, optional): News source
        url (str, optional): Article URL
    """
    # Format the date
    try:
        date_obj = datetime.fromisoformat(date.replace('Z', '+00:00'))
        formatted_date = date_obj.strftime('%b %d, %Y')
        formatted_time = date_obj.strftime('%I:%M %p')  # 12-hour format with AM/PM
        
        # Calculate time ago
        time_diff = datetime.now() - date_obj
        hours_diff = time_diff.total_seconds() / 3600
        
        if hours_diff < 1:
            time_display = "Just now"
        elif hours_diff < 24:
            hours = int(hours_diff)
            time_display = f"{hours}h ago"
        elif time_diff.days == 1:
            time_display = "Yesterday"
        elif time_diff.days < 7:
            time_display = f"{time_diff.days}d ago"
        else:
            time_display = formatted_date
            
    except:
        formatted_date = ""
        formatted_time = ""
        time_display = ""

    # Style the tags based on category
    tag_colors = {
        'Transportation': '#ff6b6b',
        'Manufacturing': '#4dabf7',
        'Inventory': '#51cf66',
        'Risk': '#ffd43b',
        'Technology': '#845ef7',
        'Sustainability': '#20c997'
    }

    # Create tag pills HTML
    tag_html = []
    for tag in tags:
        color = tag_colors.get(tag, "#666")
        tag_html.append(
            f'<span style="display:inline-block;background:{color}20;color:{color};'
            f'padding:4px 8px;border-radius:4px;font-size:12px;margin:2px">{tag}</span>'
        )

    # Card header with title and link
    header_html = f"""
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
            <h3 style="margin:0;font-size:16px;color:#2c3e50;flex:1">{title}</h3>
            {'<a href="' + url + '" target="_blank" style="color:#0066cc;text-decoration:none;'
            'font-size:14px;margin-left:8px">🔗 Read more</a>' if url else ''}
        </div>
    """

    # Metadata line with source and date
    meta_html = f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:12px;color:#666">
            {'<span style="color:#0066cc">' + source + '</span>' if source else ''}
            {'<span>•</span>' if source else ''}
            <span>{time_display}</span>
            {'<span title="' + formatted_date + ' ' + formatted_time + '" style="cursor:help">🕒</span>' if formatted_date else ''}
        </div>
    """

    # Summary text
    summary_html = f"""
        <p style="margin:0 0 12px 0;color:#666;font-size:14px;line-height:1.4">{summary}</p>
    """

    # Tags container
    tags_html = f"""
        <div style="display:flex;flex-wrap:wrap;gap:4px">{''.join(tag_html)}</div>
    """

    # Combine all parts into the card
    card_html = f"""
        <div style="background:white;border-radius:8px;padding:16px;margin-bottom:16px;
                    box-shadow:0 2px 4px rgba(0,0,0,0.05)">
            {header_html}
            {meta_html}
            {summary_html}
            {tags_html}
        </div>
    """

    # Render the card
    st.markdown(card_html, unsafe_allow_html=True) 