import re

def calculate_score(text, skills, predicted_role):
    """
    Calculates a resume score (0-100) based on various factors.
    """
    score = 0
    
    # 1. Content Length (Check if resume is too short or good length)
    word_count = len(text.split())
    if word_count > 100:
        score += 10
    if word_count > 300:
        score += 10
        
    # 2. Sections Presence
    sections = ['education', 'experience', 'projects', 'skills', 'certifications', 'summary', 'objective']
    text_lower = text.lower()
    for section in sections:
        if section in text_lower:
            score += 5  # Max 35 points if all 7 sections found
            
    # 3. Skills Count
    skill_count = len(skills)
    if skill_count >= 3:
        score += 10
    if skill_count >= 5:
        score += 10
    if skill_count >= 10:
        score += 5
        
    # 4. Keyword matching (basic implementation)
    # If we have a predicted role, we check if key terms for that role are present
    # This is partially covered by skills, but let's add a "relevance" bump
    # For now, we assume if prediction confidence was high, the content is relevant.
    # We'll just cap it at 100.
    
    # Base score normalization
    # Current max: 20 (length) + 35 (sections) + 25 (skills) = 80
    
    # Add filler points for formatting/email/phone detection
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\b\d{10}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    
    if re.search(email_pattern, text):
        score += 10
    if re.search(phone_pattern, text):
        score += 10
        
    # Cap at 100
    return min(100, score)

def get_improvement_suggestions(text, skills, score):
    suggestions = []
    
    word_count = len(text.split())
    if word_count < 300:
        suggestions.append("Your resume seems a bit short. Consider adding more details about your projects and responsibilities.")
        
    sections = ['education', 'experience', 'projects', 'skills']
    text_lower = text.lower()
    missing_sections = [s for s in sections if s not in text_lower]
    if missing_sections:
        suggestions.append(f"We couldn't clearly find these sections: {', '.join(missing_sections).title()}. Ensure they are clearly labeled.")
        
    if len(skills) < 5:
        suggestions.append("Try to list more technical and soft skills to improve matching.")
        
    if score < 70:
        suggestions.append("Overall, try to expand on your experience and use more industry-standard keywords.")
        
    return suggestions
