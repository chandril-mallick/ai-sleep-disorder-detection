import os
import joblib
import pandas as pd
import datetime

def load_model():
    """Loads the trained model and label encoder."""
    # Navigate up from 'dashboard' to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'sleep_model_fast.pkl')
    le_path = os.path.join(base_dir, 'models', 'label_encoder.pkl')
    occupation_encoder_path = os.path.join(base_dir, 'models', 'occupation_encoder.pkl')
    
    if not os.path.exists(model_path):
        return None, None, None
        
    model = joblib.load(model_path)
    le = joblib.load(le_path)
    
    # Load occupation encoder if exists
    occupation_encoder = None
    if os.path.exists(occupation_encoder_path):
        occupation_encoder = joblib.load(occupation_encoder_path)
    
    return model, le, occupation_encoder

def preprocess_input(gender, age, occupation, sleep_duration, quality_of_sleep, physical_activity, stress_level, bmi_category, heart_rate, daily_steps, bp_systolic, bp_diastolic, occupation_encoder=None):
    """Preprocesses user input into a DataFrame for the model."""
    gender_val = 0 if gender == 'Male' else 1
    bmi_map = {'Normal': 0, 'Overweight': 1, 'Obese': 2}
    bmi_val = bmi_map.get(bmi_category, 0)
    
    # Encode occupation if encoder is available
    occupation_val = 0  # Default
    if occupation_encoder is not None:
        try:
            occupation_val = occupation_encoder.transform([occupation])[0]
        except:
            # If occupation not in training data, use a default value
            occupation_val = 0

    input_data = pd.DataFrame({
        'Gender': [gender_val],
        'Age': [age],
        'Occupation': [occupation_val],
        'Sleep Duration': [sleep_duration],
        'Quality of Sleep': [quality_of_sleep],
        'Physical Activity Level': [physical_activity],
        'Stress Level': [stress_level],
        'BMI Category': [bmi_val],
        'Heart Rate': [heart_rate],
        'Daily Steps': [daily_steps],
        'BP_Systolic': [bp_systolic],
        'BP_Diastolic': [bp_diastolic]
    })
    return input_data

def get_recommendations(duration, quality, stress, activity, bmi, heart_rate):
    """Generates personalized recommendations based on health metrics."""
    recommendations = []
    
    # Sleep Duration
    if duration < 6.0:
        recommendations.append("Increase Sleep Duration: Aim for at least 7 hours. Consistent lack of sleep increases health risks.")
    elif duration > 9.0:
        recommendations.append("Regulate Sleep Pattern: Oversleeping can indicate underlying issues. Try to stick to a consistent 7-8 hour schedule.")
        
    # Sleep Quality
    if quality < 6:
        recommendations.append("Improve Sleep Hygiene: Low sleep quality detected. Avoid screens before bed, keep your room cool, and limit caffeine.")
        
    # Stress
    if stress > 6:
        recommendations.append("Manage Stress: High stress negatively impacts sleep. Consider meditation, deep breathing, or yoga.")
        
    # Physical Activity
    if activity < 30:
        recommendations.append("Get Moving: Regular physical activity (30+ mins/day) promotes deeper sleep.")
        
    # BMI
    if bmi != 'Normal':
        recommendations.append("Watch Your Weight: Maintaining a healthy weight reduces the risk of sleep apnea and insomnia.")
        
    # Heart Rate
    if heart_rate > 80:
        recommendations.append("Monitor Heart Rate: Resting heart rate is slightly high. Regular cardio and stress reduction can help.")
        
    if not recommendations:
        recommendations.append("Excellent Habits: Your metrics suggest good sleep health. Keep it up!")
        
    return recommendations

def generate_report(user_data, prediction_label, risk_val, recommendations):
    """Generates a text report of the analysis."""
    report_text = f"""
    SLEEP HEALTH ANALYSIS REPORT
    Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    ----------------------------------------
    USER PROFILE:
    - Gender: {user_data['Gender']}
    - Age: {user_data['Age']}
    - Occupation: {user_data.get('Occupation', 'N/A')}
    - BMI Category: {user_data['BMI']}
    - Sleep Duration: {user_data['Sleep Duration']} hrs
    - Sleep Quality: {user_data['Quality of Sleep']}/10
    - Stress Level: {user_data['Stress Level']}/10
    - Physical Activity: {user_data['Physical Activity']} mins/day
    - Heart Rate: {user_data['Heart Rate']} bpm
    - Daily Steps: {user_data['Daily Steps']}
    - Blood Pressure: {user_data['BP']}
    ----------------------------------------
    ANALYSIS RESULT:
    Prediction: {prediction_label}
    Risk Level: {risk_val}/100
    ----------------------------------------
    RECOMMENDATIONS:
    """
    for rec in recommendations:
        # Clean up markdown for text file
        clean_rec = rec.replace('**', '').replace(' ', '').replace(' ', '').replace(' ', '').replace(' ', '').replace(' ', '').replace(' ', '').replace(' ', '').replace(' ', '')
        report_text += f"\n- {clean_rec}"
        
    return report_text
