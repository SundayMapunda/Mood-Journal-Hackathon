import requests
import os
from flask import current_app

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