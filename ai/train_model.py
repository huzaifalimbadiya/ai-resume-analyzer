import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_model():
    # Load dataset
    if not os.path.exists('resume_dataset.csv'):
        print("Dataset not found. Please run create_dataset.py first.")
        return

    df = pd.read_csv('resume_dataset.csv')
    
    # Preprocessing (Simple for now, can be improved)
    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(max_features=3000, stop_words='english')
    X = tfidf.fit_transform(df['Resume_Text'])
    y = df['Category']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model Training (Logistic Regression)
    clf = LogisticRegression(multi_class='multinomial', solver='lbfgs')
    clf.fit(X_train, y_train)
    
    # Evaluation
    y_pred = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    # Save Model and Vectorizer
    model_path = os.path.join('trained_models', 'job_role_model.pkl')
    vectorizer_path = os.path.join('trained_models', 'tfidf_vectorizer.pkl')
    
    joblib.dump(clf, model_path)
    joblib.dump(tfidf, vectorizer_path)
    
    print(f"Model saved to {model_path}")
    print(f"Vectorizer saved to {vectorizer_path}")

if __name__ == '__main__':
    train_model()
