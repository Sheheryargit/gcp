import spacy
from typing import Dict, List, Any
import re
from collections import Counter

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def calculate_risk_score(text: str) -> float:
    """Calculate a risk score for the given text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        float: Risk score between 0 and 1
    """
    # Define risk-related keywords and their weights
    risk_keywords = {
        'high': 0.9,
        'severe': 0.9,
        'critical': 0.9,
        'urgent': 0.8,
        'warning': 0.7,
        'delay': 0.6,
        'disruption': 0.7,
        'shortage': 0.7,
        'issue': 0.5,
        'problem': 0.5,
        'concern': 0.4,
        'potential': 0.3,
        'minor': 0.2,
        'low': 0.1
    }
    
    # Normalize text
    text = text.lower()
    
    # Calculate weighted score
    total_weight = 0
    matches = 0
    
    for keyword, weight in risk_keywords.items():
        if keyword in text:
            total_weight += weight
            matches += 1
            
    # Return normalized score
    if matches == 0:
        return 0.0
    return min(1.0, total_weight / (matches * 0.9))  # Normalize by max possible weight

def extract_entities(text: str) -> Dict[str, List[str]]:
    """Extract named entities from text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        Dict[str, List[str]]: Dictionary of entity types and their values
    """
    doc = nlp(text)
    entities = {}
    
    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = []
        if ent.text not in entities[ent.label_]:
            entities[ent.label_].append(ent.text)
            
    return entities

def categorize_content(text: str) -> List[str]:
    """Categorize the content based on supply chain domains.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        List[str]: List of relevant categories
    """
    # Define category keywords
    categories = {
        'logistics': ['shipping', 'transport', 'delivery', 'freight', 'cargo'],
        'inventory': ['stock', 'inventory', 'warehouse', 'storage', 'supply'],
        'manufacturing': ['production', 'manufacturing', 'assembly', 'factory'],
        'procurement': ['sourcing', 'procurement', 'purchasing', 'supplier'],
        'quality': ['quality', 'inspection', 'compliance', 'standard'],
        'financial': ['cost', 'price', 'financial', 'budget', 'expense']
    }
    
    text = text.lower()
    matched_categories = []
    
    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            matched_categories.append(category)
            
    return matched_categories if matched_categories else ['general'] 