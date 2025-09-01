import requests
import os
# from flask import current_app, request
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

# def get_user_identifier():
#     """Custom function to identify users for rate limiting"""
#     from flask_login import current_user
#     if hasattr(current_user, 'id') and current_user.is_authenticated:
#         return f"user_{current_user.id}"
#     return get_remote_address()

# # Initialize limiter (will be configured in create_app)
# hf_limiter = Limiter(key_func=get_user_identifier)

# @hf_limiter.limit("5 per minute")  # Strict limit on Hugging Face calls

def analyze_sentiment(text):
    """
    Send text to Hugging Face sentiment analysis API and return emotion scores.
    We'll use the 'j-hartmann/emotion-english-distilroberta-base' model which returns
    multiple emotions with scores.
    """
    api_url = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
    headers = {
        "Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"
    }
    payload = {
        "inputs": text
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        results = response.json()
        
        # The API returns a list of emotions with scores
        if isinstance(results, list) and len(results) > 0:
            emotion_scores = {}
            for emotion in results[0]:
                emotion_scores[emotion['label'].lower()] = emotion['score']
            return emotion_scores
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Hugging Face API error: {e}")
        return None
    except Exception as e:
        current_app.logger.error(f"Error processing sentiment analysis: {e}")
        return None