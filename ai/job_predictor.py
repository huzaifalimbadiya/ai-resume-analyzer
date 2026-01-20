import joblib
import os
import numpy as np
from django.conf import settings

# Define paths to models
# Assuming this is called from Django context, so settings.BASE_DIR is available
# But to be safe, we can use relative paths if running as script, or absolute if in Django.
# Let's try to find the models relative to this file.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'trained_models', 'job_role_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'trained_models', 'tfidf_vectorizer.pkl')

_model = None
_vectorizer = None

def load_models():
    global _model, _vectorizer
    if _model is None:
        try:
            _model = joblib.load(MODEL_PATH)
            _vectorizer = joblib.load(VECTORIZER_PATH)
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    return True

def predict_job_role(text):
    """
    Predicts the job role based on the resume text.
    Returns: (Predicted Role, Confidence Score)
    """
    if not load_models():
        return "Unknown", 0.0
        
    try:
        # Transform text
        features = _vectorizer.transform([text])
        
        # Predict
        prediction = _model.predict(features)[0]
        probabilities = _model.predict_proba(features)[0]
        confidence = np.max(probabilities)
        
        return prediction, round(confidence * 100, 2)
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Error", 0.0

def get_missing_skills(predicted_role, current_skills):
    """
    Suggests missing skills based on the predicted role.
    """
    # This should ideally come from the same logic as dataset creation or a separate DB
    role_skills = {
        'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Git', 'API'],
        'Data Analyst': ['Python', 'SQL', 'Pandas', 'Excel', 'Tableau', 'Statistics'],
        'Software Tester': ['Selenium', 'Manual Testing', 'JIRA', 'Automation', 'SQL'],
        'Designer': ['Photoshop', 'Illustrator', 'Figma', 'UI/UX', 'Wireframing'],
        'Python Developer': ['Python', 'Django', 'Flask', 'SQL', 'Git', 'Pandas'],
        'Java Developer': ['Java', 'Spring', 'Hibernate', 'SQL', 'OOP', 'Maven']
    }
    
    if predicted_role not in role_skills:
        return []
        
    expected_skills = set(role_skills[predicted_role])
    current_skills_set = set(current_skills)
    
    missing = list(expected_skills - current_skills_set)
    return missing
