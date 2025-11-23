import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Sleep Health Predictor",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Cream & Premium Theme ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #FDFBF7; /* Cream */
        color: #2C3E50; /* Dark Blue-Grey Text */
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F4F1EA; /* Slightly darker cream */
        border-right: 1px solid #E0DCD3;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #2C3E50;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
    }
    
    h1 {
        color: #1A252F;
        border-bottom: 2px solid #D4AF37; /* Gold Accent */
        padding-bottom: 10px;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #D4AF37; /* Gold */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #B5952F; /* Darker Gold */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Cards/Containers */
    .css-1r6slb0 {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #D4AF37;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 5px;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Load model and encoder
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'sleep_model_fast.pkl')
    le_path = os.path.join(base_dir, 'models', 'label_encoder.pkl')
    
    if not os.path.exists(model_path):
        return None, None
        
    model = joblib.load(model_path)
    le = joblib.load(le_path)
    return model, le

def get_recommendations(duration, quality, stress, activity, bmi, heart_rate):
    recommendations = []
    
    # Sleep Duration
    if duration < 6.0:
        recommendations.append("⚠️ **Increase Sleep Duration**: Aim for at least 7 hours of sleep. Consistent lack of sleep increases health risks.")
    elif duration > 9.0:
        recommendations.append("ℹ️ **Regulate Sleep Pattern**: Oversleeping can sometimes indicate underlying issues. Try to stick to a consistent 7-8 hour schedule.")
        
    # Sleep Quality
    if quality < 6:
        recommendations.append("🌙 **Improve Sleep Hygiene**: Your sleep quality is low. Avoid screens before bed, keep your room cool, and limit caffeine.")
        
    # Stress
    if stress > 6:
        recommendations.append("🧘 **Manage Stress**: High stress negatively impacts sleep. Consider meditation, deep breathing exercises, or yoga.")
        
    # Physical Activity
    if activity < 30:
        recommendations.append("🏃 **Get Moving**: Regular physical activity (at least 30 mins/day) promotes deeper sleep.")
        
    # BMI
    if bmi != 'Normal':
        recommendations.append("🍎 **Watch Your Weight**: Maintaining a healthy weight can significantly reduce the risk of sleep apnea and insomnia.")
        
    # Heart Rate
    if heart_rate > 80:
        recommendations.append("❤️ **Monitor Heart Rate**: Your resting heart rate is slightly high. Regular cardio and stress reduction can help.")
        
    if not recommendations:
        recommendations.append("✅ **Keep it up!**: Your habits seem conducive to good sleep health.")
        
    return recommendations

model, le = load_model()

# --- Header Section ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title(' Sleep Health Predictor')
    st.markdown("### AI-Powered Sleep Disorder Risk Analysis")
    st.markdown("Enter your health metrics to receive a personalized assessment of your sleep health.")

with col2:
    # Placeholder for a logo or icon if needed
    st.write("") 

st.markdown("---")

# --- Main Layout ---
col_input, col_viz = st.columns([1, 2], gap="large")

with col_input:
    st.subheader("Your Health Profile")
    with st.container():
        st.markdown("Please fill in your details below:")
        
        gender = st.selectbox('Gender', ['Male', 'Female'])
        age = st.slider('Age', 10, 100, 30)
        bmi_category = st.selectbox('BMI Category', ['Normal', 'Overweight', 'Obese'])
        
        st.markdown("---")
        st.markdown("**Sleep & Activity**")
        sleep_duration = st.slider('Sleep Duration (Hours)', 0.0, 12.0, 7.0, 0.1)
        quality_of_sleep = st.slider('Quality of Sleep (1-10)', 1, 10, 6)
        physical_activity = st.slider('Physical Activity (mins/day)', 0, 120, 30)
        daily_steps = st.number_input('Daily Steps', 0, 20000, 5000, step=100)
        
        st.markdown("---")
        st.markdown("**Vitals**")
        stress_level = st.slider('Stress Level (1-10)', 1, 10, 5)
        heart_rate = st.slider('Heart Rate (bpm)', 40, 120, 70)
        col_bp1, col_bp2 = st.columns(2)
        with col_bp1:
            bp_systolic = st.number_input('Systolic BP', 80, 200, 120)
        with col_bp2:
            bp_diastolic = st.number_input('Diastolic BP', 50, 130, 80)

# Preprocess inputs
gender_val = 0 if gender == 'Male' else 1
bmi_map = {'Normal': 0, 'Overweight': 1, 'Obese': 2}
bmi_val = bmi_map[bmi_category]

input_data = pd.DataFrame({
    'Gender': [gender_val],
    'Age': [age],
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

with col_viz:
    st.subheader(" Health Analysis Dashboard")
    
    # Radar Chart for Metrics
    categories = ['Sleep Quality', 'Activity Level', 'Stress Control', 'Heart Health', 'Sleep Duration']
    
    # Normalize values for radar chart (0-1 scale approx for visualization)
    # This is just for visual representation
    r_sleep_qual = quality_of_sleep / 10
    r_activity = min(physical_activity / 90, 1.0) # Assume 90 is good
    r_stress = 1 - (stress_level / 10) # Lower stress is better
    r_heart = 1 - (abs(heart_rate - 70) / 50) # Closer to 70 is better
    r_duration = min(sleep_duration / 8, 1.0) # 8 hours is target
    
    r_values = [r_sleep_qual, r_activity, r_stress, r_heart, r_duration]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_values,
        theta=categories,
        fill='toself',
        name='Your Profile',
        line_color='#D4AF37',
        fillcolor='rgba(212, 175, 55, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=20, b=20),
        height=300
    )
    
    st.plotly_chart(fig, width="stretch")
    
    # Prediction Section
    st.markdown("### Risk Assessment")
    
    if st.button('Analyze Risk', width="stretch"):
        if model:
            prediction = model.predict(input_data)
            prediction_label = le.inverse_transform(prediction)[0]
            
            # Result Display
            result_container = st.container()
            
            if prediction_label == 'Healthy':
                result_color = "#27AE60" # Green
                result_msg = "Excellent! Your sleep health indicators are strong."
                result_icon = "🌿"
            elif prediction_label == 'Sleep Apnea':
                result_color = "#E74C3C" # Red
                result_msg = "High Risk Detected. We recommend consulting a healthcare provider."
                result_icon = "⚠️"
            elif prediction_label == 'Insomnia':
                result_color = "#F39C12" # Orange
                result_msg = "Signs of Insomnia detected. Consider reviewing your sleep hygiene."
                result_icon = "🌙"
            else:
                result_color = "#3498DB"
                result_msg = "Analysis Complete."
                result_icon = "ℹ️"
                
            st.markdown(f"""
                <div style="
                    background-color: {result_color}20;
                    border-left: 5px solid {result_color};
                    padding: 20px;
                    border-radius: 5px;
                    margin-top: 20px;">
                    <h2 style="color: {result_color}; margin:0;">{result_icon} {prediction_label}</h2>
                    <p style="font-size: 1.1em; margin-top: 10px;">{result_msg}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Gauge Chart for Risk (Simulated based on label)
            risk_val = 0
            if prediction_label == 'Healthy': risk_val = 20
            elif prediction_label == 'Insomnia': risk_val = 60
            elif prediction_label == 'Sleep Apnea': risk_val = 90
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_val,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Estimated Risk Level"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': result_color},
                    'steps': [
                        {'range': [0, 33], 'color': "#E8F5E9"},
                        {'range': [33, 66], 'color': "#FFF3E0"},
                        {'range': [66, 100], 'color': "#FFEBEE"}],
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_gauge, width="stretch")
            
            # --- Smart Recommendations ---
            st.markdown("### AI Health Insights")
            recommendations = get_recommendations(sleep_duration, quality_of_sleep, stress_level, physical_activity, bmi_category, heart_rate)
            
            with st.expander("View Personalized Recommendations", expanded=True):
                for rec in recommendations:
                    st.markdown(f"- {rec}")
            
            # --- Download Report ---
            import datetime
            report_text = f"""
            SLEEP HEALTH ANALYSIS REPORT
            Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            ----------------------------------------
            USER PROFILE:
            - Gender: {gender}
            - Age: {age}
            - BMI Category: {bmi_category}
            - Sleep Duration: {sleep_duration} hrs
            - Sleep Quality: {quality_of_sleep}/10
            - Stress Level: {stress_level}/10
            - Physical Activity: {physical_activity} mins/day
            - Heart Rate: {heart_rate} bpm
            - Daily Steps: {daily_steps}
            - Blood Pressure: {bp_systolic}/{bp_diastolic}
            ----------------------------------------
            ANALYSIS RESULT:
            Prediction: {prediction_label}
            Risk Level: {risk_val}/100
            ----------------------------------------
            RECOMMENDATIONS:
            """
            for rec in recommendations:
                report_text += f"\n{rec.replace('**', '').replace('⚠️ ', '').replace('ℹ️ ', '').replace('🌙 ', '').replace('🧘 ', '').replace('🏃 ', '').replace('🍎 ', '').replace('❤️ ', '').replace('✅ ', '')}"
            
            st.download_button(
                label="Download Full Report",
                data=report_text,
                file_name=f"Sleep_Health_Report_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
            )
            
        else:
            st.error("Model could not be loaded. Please ensure the model files are present.")
    else:
        st.info("Adjust the sliders on the left and click 'Analyze Risk' to see your results.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7F8C8D; font-size: 0.8em;'>"
    "Samsung Capstone Sleep Project | Designed for Better Health"
    "</div>", 
    unsafe_allow_html=True
)

