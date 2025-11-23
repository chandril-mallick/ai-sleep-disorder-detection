import streamlit as st
import plotly.graph_objects as go
from styles import get_css
from utils import load_model, preprocess_input, get_recommendations, generate_report
import datetime
import pandas as pd
import numpy as np

# Page Config
st.set_page_config(
    page_title="Sleep Health Predictor | Professional Edition",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject CSS
st.markdown(get_css(), unsafe_allow_html=True)

# Load Model
model, le, occupation_encoder = load_model()

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/sleep.png", width=60)
    st.title("Patient Data")
    st.markdown("Enter patient metrics below.")
    
    # Smartwatch Connection Section
    st.markdown("---")
    st.markdown("### Device Connection")
    
    # Initialize connection state
    if 'watch_connected' not in st.session_state:
        st.session_state['watch_connected'] = False
    if 'watch_syncing' not in st.session_state:
        st.session_state['watch_syncing'] = False
    
    # Device selection
    device_options = ['Samsung Galaxy Watch', 'Apple Watch', 'Fitbit', 'Garmin', 'Other']
    selected_device = st.selectbox('Select Device', device_options, disabled=st.session_state['watch_connected'])
    
    # Connection button
    if not st.session_state['watch_connected']:
        if st.button("Connect to Smartwatch", width="stretch"):
            st.session_state['watch_syncing'] = True
            st.session_state['watch_connected'] = True
            st.rerun()
    else:
        st.success(f"Connected: {selected_device}")
        if st.button("Disconnect", width="stretch"):
            st.session_state['watch_connected'] = False
            st.session_state['watch_syncing'] = False
            st.rerun()
        
        # Sync data button
        if st.button("Sync Data", width="stretch"):
            st.session_state['watch_syncing'] = True
            st.rerun()
    
    # Show syncing animation
    if st.session_state.get('watch_syncing', False):
        with st.spinner('Syncing data from smartwatch...'):
            import time
            time.sleep(2)  # Simulate sync delay
            st.session_state['watch_syncing'] = False
            st.session_state['synced_data'] = {
                'heart_rate': np.random.randint(60, 85),
                'steps': np.random.randint(4000, 12000),
                'sleep_duration': round(np.random.uniform(6.0, 8.5), 1),
                'sleep_quality': np.random.randint(6, 9)
            }
            st.success("Data synced successfully!")
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### Demographics")
    gender = st.selectbox('Gender', ['Male', 'Female'])
    age = st.slider('Age', 10, 100, 30)
    occupation = st.selectbox('Occupation', [
        'Software Engineer', 'Doctor', 'Sales Representative', 'Teacher', 
        'Nurse', 'Engineer', 'Accountant', 'Scientist', 'Lawyer', 
        'Salesperson', 'Manager', 'Student', 'Other'
    ])
    bmi_category = st.selectbox('BMI Category', ['Normal', 'Overweight', 'Obese'])
    
    st.markdown("### Sleep & Activity")
    
    # Use synced data if available
    synced_data = st.session_state.get('synced_data', {})
    default_sleep = synced_data.get('sleep_duration', 7.0)
    default_quality = synced_data.get('sleep_quality', 6)
    default_steps = synced_data.get('steps', 5000)
    
    sleep_duration = st.slider('Sleep Duration (Hours)', 0.0, 12.0, float(default_sleep), 0.1)
    quality_of_sleep = st.slider('Quality of Sleep (1-10)', 1, 10, default_quality)
    physical_activity = st.slider('Physical Activity (mins/day)', 0, 120, 30)
    daily_steps = st.number_input('Daily Steps', 0, 20000, default_steps, step=100)
    
    st.markdown("### Vitals")
    
    default_hr = synced_data.get('heart_rate', 70)
    
    stress_level = st.slider('Stress Level (1-10)', 1, 10, 5)
    heart_rate = st.slider('Heart Rate (bpm)', 40, 120, default_hr)
    
    st.markdown("### Blood Pressure")
    col_bp1, col_bp2 = st.columns(2)
    with col_bp1:
        bp_systolic = st.number_input('Systolic', 80, 200, 120, key='sys')
    with col_bp2:
        bp_diastolic = st.number_input('Diastolic', 50, 130, 80, key='dia')

# --- Main Content ---
st.title("Sleep Health Analysis Dashboard")
st.markdown("### AI-Powered Clinical Support System")

# Show sync status
if st.session_state.get('watch_connected', False):
    col_status1, col_status2, col_status3 = st.columns([2, 1, 1])
    with col_status1:
        st.info(f"📱 **Device Connected:** {selected_device}")
    with col_status2:
        if 'synced_data' in st.session_state:
            st.success("✅ Data Synced")
        else:
            st.warning("⏳ No Data Yet")
    with col_status3:
        last_sync = datetime.datetime.now().strftime("%H:%M")
        st.caption(f"Last sync: {last_sync}")

if not model:
    st.error(" Model not found. Please train the model first.")
    st.stop()

# Calculate Sleep Score (0-100)
def calculate_sleep_score(duration, quality, stress, activity, heart_rate):
    score = 0
    # Duration (30 points)
    if 7 <= duration <= 9:
        score += 30
    elif 6 <= duration < 7 or 9 < duration <= 10:
        score += 20
    else:
        score += 10
    
    # Quality (25 points)
    score += (quality / 10) * 25
    
    # Stress (20 points)
    score += ((10 - stress) / 10) * 20
    
    # Activity (15 points)
    if activity >= 30:
        score += 15
    else:
        score += (activity / 30) * 15
    
    # Heart Rate (10 points)
    if 60 <= heart_rate <= 80:
        score += 10
    else:
        score += max(0, 10 - abs(heart_rate - 70) / 5)
    
    return min(100, round(score))

sleep_score = calculate_sleep_score(sleep_duration, quality_of_sleep, stress_level, physical_activity, heart_rate)

# Prepare Input
input_df = preprocess_input(
    gender, age, occupation, sleep_duration, quality_of_sleep, physical_activity, 
    stress_level, bmi_category, heart_rate, daily_steps, bp_systolic, bp_diastolic,
    occupation_encoder
)

# Top Metrics Row
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Sleep Score", f"{sleep_score}/100", 
              delta="Good" if sleep_score >= 70 else "Needs Improvement",
              delta_color="normal" if sleep_score >= 70 else "inverse")
with col_m2:
    st.metric("Sleep Duration", f"{sleep_duration}h", 
              delta="Optimal" if 7 <= sleep_duration <= 9 else "Adjust")
with col_m3:
    st.metric("Activity Level", f"{physical_activity}min", 
              delta="Active" if physical_activity >= 30 else "Low")
with col_m4:
    st.metric("Stress Level", f"{stress_level}/10", 
              delta="High" if stress_level > 6 else "Managed",
              delta_color="inverse" if stress_level > 6 else "normal")

st.markdown("---")

# Layout: 2 Columns
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("Analysis Results")
    
    if st.button("Run Analysis", width="stretch"):
        # Prediction
        prediction = model.predict(input_df)
        prediction_label = le.inverse_transform(prediction)[0]
        
        # Validation Layer - Override model if obvious issues detected
        if sleep_duration < 5:
            prediction_label = 'Insomnia'
        elif sleep_duration > 10:
            prediction_label = 'Sleep Apnea'
        elif stress_level >= 9 and quality_of_sleep <= 3:
            prediction_label = 'Insomnia'
        elif heart_rate > 100 or heart_rate < 50:
            if prediction_label == 'Healthy':
                prediction_label = 'Sleep Apnea'
        
        # Risk Calculation
        risk_val = 0
        if prediction_label == 'Healthy': risk_val = 15
        elif prediction_label == 'Insomnia': risk_val = 65
        elif prediction_label == 'Sleep Apnea': risk_val = 92
        
        # Store in history
        st.session_state['history'].append({
            'timestamp': datetime.datetime.now(),
            'prediction': prediction_label,
            'risk': risk_val,
            'score': sleep_score
        })
        
        # Display Result
        if prediction_label == 'Healthy':
            st.success(f"### Diagnosis: {prediction_label}\nPatient shows no signs of sleep disorders.")
        elif prediction_label == 'Sleep Apnea':
            st.error(f"### Diagnosis: {prediction_label}\nHigh probability of Sleep Apnea. Clinical consultation recommended.")
        else:
            st.warning(f"### Diagnosis: {prediction_label}\nSymptoms consistent with Insomnia. Monitor sleep hygiene.")
        
        # Recommendations
        st.markdown("#### AI Recommendations")
        recs = get_recommendations(sleep_duration, quality_of_sleep, stress_level, physical_activity, bmi_category, heart_rate)
        
        with st.expander("View Personalized Recommendations", expanded=True):
            for rec in recs:
                st.info(rec)
        
        # Generate Report
        user_data_dict = {
            'Gender': gender, 'Age': age, 'Occupation': occupation, 'BMI': bmi_category,
            'Sleep Duration': sleep_duration, 'Quality of Sleep': quality_of_sleep,
            'Physical Activity': physical_activity, 'Stress Level': stress_level,
            'Heart Rate': heart_rate, 'Daily Steps': daily_steps,
            'BP': f"{bp_systolic}/{bp_diastolic}"
        }
        report_txt = generate_report(user_data_dict, prediction_label, risk_val, recs)
        
        st.download_button(
            label="Download Clinical Report",
            data=report_txt,
            file_name=f"Clinical_Report_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
        )
        
        st.session_state['risk_val'] = risk_val
        st.session_state['prediction'] = prediction_label
        st.session_state['run'] = True

with col_right:
    st.subheader(" Health Metrics Visualization")
    
    # Radar Chart with Baseline Comparison
    categories = ['Sleep Quality', 'Activity', 'Stress Mgmt', 'Heart Health', 'Sleep Duration']
    
    # Current values
    r_values = [
        quality_of_sleep / 10,
        min(physical_activity / 90, 1.0),
        1 - (stress_level / 10),
        1 - (abs(heart_rate - 70) / 50),
        min(sleep_duration / 8, 1.0)
    ]
    
    # Healthy baseline
    baseline = [0.8, 0.7, 0.8, 0.9, 0.9]
    
    fig = go.Figure()
    
    # Add baseline
    fig.add_trace(go.Scatterpolar(
        r=baseline,
        theta=categories,
        fill='toself',
        name='Healthy Baseline',
        line_color='#4ADE80',
        fillcolor='rgba(74, 222, 128, 0.1)'
    ))
    
    # Add current
    fig.add_trace(go.Scatterpolar(
        r=r_values,
        theta=categories,
        fill='toself',
        name='Your Profile',
        line_color='#00D9FF',
        fillcolor='rgba(0, 217, 255, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1]),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=40, b=20),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA')
    )
    
    st.plotly_chart(fig, width="stretch")
    
    # Gauge Chart
    if 'run' in st.session_state and st.session_state['run']:
        risk = st.session_state['risk_val']
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = risk,
            delta = {'reference': 50},
            title = {'text': "Risk Assessment Score", 'font': {'color': '#FAFAFA'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': '#FAFAFA'},
                'bar': {'color': "#00D9FF"},
                'bgcolor': '#1A1D24',
                'borderwidth': 2,
                'bordercolor': '#2D3139',
                'steps': [
                    {'range': [0, 33], 'color': "#1A3A2A"},
                    {'range': [33, 66], 'color': "#3A2A1A"},
                    {'range': [66, 100], 'color': "#3A1A1A"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig_gauge.update_layout(
            height=250, 
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FAFAFA')
        )
        st.plotly_chart(fig_gauge, width="stretch")

# Historical Tracking
if len(st.session_state['history']) > 0:
    st.markdown("---")
    st.subheader("Historical Analysis")
    
    col_h1, col_h2 = st.columns([2, 1])
    
    with col_h1:
        # Trend Chart
        history_df = pd.DataFrame(st.session_state['history'])
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=history_df['timestamp'],
            y=history_df['score'],
            mode='lines+markers',
            name='Sleep Score',
            line=dict(color='#00D9FF', width=3),
            marker=dict(size=8)
        ))
        
        fig_trend.update_layout(
            title="Sleep Score Trend",
            xaxis_title="Time",
            yaxis_title="Score",
            height=250,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FAFAFA'),
            xaxis=dict(gridcolor='#2D3139'),
            yaxis=dict(gridcolor='#2D3139')
        )
        
        st.plotly_chart(fig_trend, width="stretch")
    
    with col_h2:
        st.markdown("**Analysis Summary**")
        avg_score = np.mean([h['score'] for h in st.session_state['history']])
        st.metric("Average Score", f"{avg_score:.1f}/100")
        st.metric("Total Analyses", len(st.session_state['history']))
        
        if st.button("Clear History"):
            st.session_state['history'] = []
            st.rerun()

# Feature Importance Section
st.markdown("---")
st.subheader("Feature Importance Analysis")

col_fi1, col_fi2 = st.columns([1, 1])

with col_fi1:
    st.markdown("**What Factors Most Affect Sleep Health?**")
    
    # Get feature importances from the model
    if model and hasattr(model, 'feature_importances_'):
        feature_names = ['Gender', 'Age', 'Occupation', 'Sleep Duration', 'Quality of Sleep', 
                        'Physical Activity', 'Stress Level', 'BMI Category', 'Heart Rate', 
                        'Daily Steps', 'BP Systolic', 'BP Diastolic']
        importances = model.feature_importances_
        
        # Create DataFrame and sort
        fi_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=True)
        
        # Create horizontal bar chart
        fig_fi = go.Figure(go.Bar(
            x=fi_df['Importance'],
            y=fi_df['Feature'],
            orientation='h',
            marker=dict(
                color=fi_df['Importance'],
                colorscale='Teal',
                showscale=False
            )
        ))
        
        fig_fi.update_layout(
            title="Feature Importance Scores",
            xaxis_title="Importance",
            yaxis_title="",
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FAFAFA'),
            xaxis=dict(gridcolor='#2D3139'),
            yaxis=dict(gridcolor='#2D3139')
        )
        
        st.plotly_chart(fig_fi, width="stretch")

with col_fi2:
    st.markdown("**Understanding the Results**")
    st.info("""
    **Feature Importance** shows which health metrics have the strongest influence on sleep disorder predictions.
    
    **Higher bars** = More important for prediction
    
    **Key Insights:**
    - Focus on improving the top-ranked factors
    - These metrics have the biggest impact on your sleep health
    - The model weighs these features most heavily in its decision
    """)
    
    # Top 3 features
    top_3 = fi_df.tail(3)
    st.markdown("**Top 3 Most Important Factors:**")
    for idx, row in top_3.iterrows():
        st.markdown(f"🔹 **{row['Feature']}** ({row['Importance']:.3f})")

# What-If Simulator
st.markdown("---")
st.subheader("What-If Simulator")
st.markdown("**Explore how changing your habits could affect your sleep health**")

col_sim1, col_sim2 = st.columns([1, 1])

with col_sim1:
    st.markdown("**Adjust Metrics to See Impact**")
    
    sim_sleep = st.slider('Simulated Sleep Duration (hrs)', 0.0, 12.0, float(sleep_duration), 0.5, key='sim_sleep')
    sim_quality = st.slider('Simulated Sleep Quality', 1, 10, quality_of_sleep, key='sim_quality')
    sim_stress = st.slider('Simulated Stress Level', 1, 10, stress_level, key='sim_stress')
    sim_activity = st.slider('Simulated Physical Activity (mins)', 0, 120, physical_activity, key='sim_activity')
    
    if st.button("Run Simulation", key='sim_button'):
        # Calculate simulated score
        sim_score = calculate_sleep_score(sim_sleep, sim_quality, sim_stress, sim_activity, heart_rate)
        
        # Prepare simulated input
        sim_input = preprocess_input(
            gender, age, occupation, sim_sleep, sim_quality, sim_activity, 
            stress_level, bmi_category, heart_rate, daily_steps, bp_systolic, bp_diastolic,
            occupation_encoder
        )
        
        # Get prediction
        sim_prediction = model.predict(sim_input)
        sim_label = le.inverse_transform(sim_prediction)[0]
        
        # Store in session state
        st.session_state['sim_score'] = sim_score
        st.session_state['sim_label'] = sim_label
        st.session_state['sim_run'] = True

with col_sim2:
    if 'sim_run' in st.session_state and st.session_state['sim_run']:
        st.markdown("**Simulation Results**")
        
        # Compare scores
        score_diff = st.session_state['sim_score'] - sleep_score
        
        col_comp1, col_comp2 = st.columns(2)
        with col_comp1:
            st.metric("Current Score", f"{sleep_score}/100")
            st.metric("Current Status", st.session_state.get('prediction', 'N/A'))
        
        with col_comp2:
            st.metric("Simulated Score", f"{st.session_state['sim_score']}/100", 
                     delta=f"{score_diff:+.0f}")
            st.metric("Simulated Status", st.session_state['sim_label'])
        
        # Interpretation
        if score_diff > 10:
            st.success("✅ **Great improvement!** These changes could significantly boost your sleep health.")
        elif score_diff > 0:
            st.info("📈 **Positive change.** These adjustments would help improve your sleep.")
        elif score_diff < -10:
            st.error("⚠️ **Decline detected.** These changes could worsen your sleep health.")
        else:
            st.warning("➡️ **Minimal change.** Try adjusting other factors for better results.")
    else:
        st.info("👆 Adjust the sliders above and click 'Run Simulation' to see how changes affect your sleep health.")


