import pandas as pd
import random

def create_synthetic_dataset():
    data = []
    
    # Skills and keywords for different roles
    roles = {
        'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue', 'Django', 'Flask', 'Node.js', 'SQL', 'Git', 'API', 'REST', 'Frontend', 'Backend'],
        'Data Analyst': ['Python', 'SQL', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'Tableau', 'Power BI', 'Excel', 'Statistics', 'Data Visualization', 'Cleaning', 'EDA'],
        'Software Tester': ['Selenium', 'Manual Testing', 'Automation', 'JIRA', 'Bug Tracking', 'Test Cases', 'JUnit', 'PyTest', 'QTP', 'LoadRunner', 'Regression Testing'],
        'Designer': ['Photoshop', 'Illustrator', 'Figma', 'Sketch', 'InDesign', 'UI/UX', 'Wireframing', 'Prototyping', 'User Research', 'Adobe XD', 'Creative'],
        'Python Developer': ['Python', 'Django', 'Flask', 'FastAPI', 'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'Keras', 'PyTorch', 'Scripting', 'Automation'],
        'Java Developer': ['Java', 'Spring', 'Hibernate', 'Maven', 'Gradle', 'J2EE', 'JSP', 'Servlets', 'JDBC', 'Microservices', 'OOP', 'Multithreading']
    }
    
    # Generate 500 samples
    for _ in range(500):
        role = random.choice(list(roles.keys()))
        skills = roles[role]
        
        # Pick 5-10 random skills from the role
        selected_skills = random.sample(skills, k=random.randint(5, len(skills)))
        
        # Create a "resume text"
        text = f"I am a passionate {role} with experience in {', '.join(selected_skills)}. I have worked on various projects using these technologies. I am looking for a challenging role."
        
        # Add some random noise or common words
        common_words = ["Team player", "Communication", "Problem solving", "Hardworking", "Degree in Computer Science"]
        text += " " + " ".join(random.sample(common_words, k=2))
        
        data.append({'Resume_Text': text, 'Category': role})
        
    df = pd.DataFrame(data)
    df.to_csv('resume_dataset.csv', index=False)
    print("Dataset created: resume_dataset.csv")

if __name__ == '__main__':
    create_synthetic_dataset()
