import re

# Predefined skill dataset
SKILL_DB = [
    # Programming Languages
    'Python', 'Java', 'C++', 'C', 'C#', 'JavaScript', 'TypeScript', 'Ruby', 'Swift', 'Kotlin', 'Go', 'Rust', 'PHP',
    # Web Frameworks
    'Django', 'Flask', 'FastAPI', 'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Spring Boot', 'Laravel', 'ASP.NET',
    # Data Science & ML
    'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'Scikit-learn', 'TensorFlow', 'Keras', 'PyTorch', 'NLTK', 'Spacy', 'OpenCV',
    # Databases
    'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Oracle', 'Redis', 'Cassandra',
    # DevOps & Tools
    'Git', 'GitHub', 'GitLab', 'Docker', 'Kubernetes', 'Jenkins', 'AWS', 'Azure', 'GCP', 'Linux', 'Bash',
    # Other
    'HTML', 'CSS', 'SASS', 'Bootstrap', 'Tailwind', 'JIRA', 'Selenium', 'Excel', 'Tableau', 'Power BI'
]

def extract_skills(text):
    """
    Extracts skills from the text based on the SKILL_DB.
    """
    extracted_skills = set()
    
    # Normalize text to lowercase for matching, but keep original for display if needed
    # Actually, let's just use regex with ignorecase
    
    for skill in SKILL_DB:
        # strict matching to avoid substrings (e.g., 'C' inside 'Clean')
        # \b ensures word boundary
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            extracted_skills.add(skill)
            
    return list(extracted_skills)
