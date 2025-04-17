from flask import Blueprint, jsonify, request, current_app
from ..utils.api_utils import calculate_risk_score, extract_entities, categorize_content
from typing import Dict, List, Any

risk_bp = Blueprint('risk', __name__)

@risk_bp.route('/analyze', methods=['POST'])
def analyze_text():
    """Analyze text for supply chain risks.
    
    Request Body:
        text (str): Text content to analyze
        
    Returns:
        JSON response containing risk analysis results
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text'
            }), 400
            
        text = data['text']
        
        # Perform analysis
        analysis_results = {
            'risk_score': calculate_risk_score(text),
            'entities': extract_entities(text),
            'categories': categorize_content(text)
        }
        
        # Add risk level based on score
        score = analysis_results['risk_score']
        if score < 0.3:
            risk_level = 'low'
        elif score < 0.7:
            risk_level = 'medium'
        else:
            risk_level = 'high'
            
        analysis_results['risk_level'] = risk_level
        
        return jsonify(analysis_results), 200
        
    except Exception as e:
        current_app.logger.error(f"Error analyzing text: {str(e)}")
        return jsonify({
            'error': 'Failed to analyze text',
            'message': str(e)
        }), 500

@risk_bp.route('/batch-analyze', methods=['POST'])
def batch_analyze():
    """Analyze multiple text items for supply chain risks.
    
    Request Body:
        texts (List[str]): List of text content to analyze
        
    Returns:
        JSON response containing risk analysis results for each text
    """
    try:
        data = request.get_json()
        if not data or 'texts' not in data:
            return jsonify({
                'error': 'Missing required field: texts'
            }), 400
            
        texts = data['texts']
        if not isinstance(texts, list):
            return jsonify({
                'error': 'texts field must be a list'
            }), 400
            
        # Analyze each text
        results = []
        for text in texts:
            analysis = {
                'text': text,
                'risk_score': calculate_risk_score(text),
                'entities': extract_entities(text),
                'categories': categorize_content(text)
            }
            
            # Add risk level
            score = analysis['risk_score']
            if score < 0.3:
                risk_level = 'low'
            elif score < 0.7:
                risk_level = 'medium'
            else:
                risk_level = 'high'
                
            analysis['risk_level'] = risk_level
            results.append(analysis)
            
        return jsonify({
            'results': results,
            'total_analyzed': len(results)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error performing batch analysis: {str(e)}")
        return jsonify({
            'error': 'Failed to perform batch analysis',
            'message': str(e)
        }), 500 