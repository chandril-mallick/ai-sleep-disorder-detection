import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def train():
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'raw', 'Sleep_health_and_lifestyle_dataset.csv')
    model_path = os.path.join(base_dir, 'models', 'sleep_model_fast.pkl')
    le_path = os.path.join(base_dir, 'models', 'label_encoder.pkl')

    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)

    # 1. Data Preprocessing
    
    # Drop Person ID
    if 'Person ID' in df.columns:
        df = df.drop(columns=['Person ID'])

    # Handle Gender: Convert to 0/1
    gender_map = {'Male': 0, 'Female': 1}
    df['Gender'] = df['Gender'].map(gender_map)
    df['Gender'] = df['Gender'].fillna(0) 

    # Handle Occupation: Label Encoding
    from sklearn.preprocessing import LabelEncoder
    if 'Occupation' in df.columns:
        occupation_encoder = LabelEncoder()
        df['Occupation'] = occupation_encoder.fit_transform(df['Occupation'].fillna('Other'))
        # Save occupation encoder for later use
        occupation_encoder_path = os.path.join(base_dir, 'models', 'occupation_encoder.pkl')
        joblib.dump(occupation_encoder, occupation_encoder_path)
        print(f"Occupation classes: {occupation_encoder.classes_}")

    # Handle BMI Category: 0=Normal, 1=Overweight, 2=Obese
    bmi_map = {'Normal': 0, 'Normal Weight': 0, 'Overweight': 1, 'Obese': 2}
    df['BMI Category'] = df['BMI Category'].map(bmi_map)
    
    # Handle Blood Pressure: Split '126/83'
    df[['BP_Systolic', 'BP_Diastolic']] = df['Blood Pressure'].str.split('/', expand=True).astype(int)
    df = df.drop(columns=['Blood Pressure'])

    # Target Variable: Sleep Disorder
    # Replace NaN/None with 'Healthy'
    df['Sleep Disorder'] = df['Sleep Disorder'].fillna('Healthy')
    df['Sleep Disorder'] = df['Sleep Disorder'].replace('None', 'Healthy')
    
    # Encode Target
    le = LabelEncoder()
    df['Sleep Disorder'] = le.fit_transform(df['Sleep Disorder'])
    
    print("Target Classes:", le.classes_)

    # 2. Model Training
    X = df.drop(columns=['Sleep Disorder'])
    y = df['Sleep Disorder']
    
    print("Features:", X.columns.tolist())

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest Classifier...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # Evaluation
    y_pred = rf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # 3. Saving
    print(f"Saving model to {model_path}...")
    joblib.dump(rf, model_path)
    joblib.dump(le, le_path)
    print("Done.")

if __name__ == "__main__":
    train()
