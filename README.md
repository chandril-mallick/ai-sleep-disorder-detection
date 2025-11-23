## Sleep disorder detection using wearable data


An AI-powered clinical decision support system for sleep disorder detection and health monitoring, featuring smartwatch integration and advanced analytics.

## 🌐 Live Demo

**Try it now:** [https://ai-sleep-disorder-detection.streamlit.app/](https://ai-sleep-disorder-detection.streamlit.app/)

## 🎯 Project Overview

This application uses machine learning to predict sleep disorders (Healthy, Insomnia, Sleep Apnea) based on patient health metrics. It features a professional dark-themed dashboard with real-time data visualization, smartwatch connectivity simulation, and personalized health recommendations.

## ✨ Key Features

### 🤖 AI-Powered Analysis
- **Random Forest Classifier** with 88% accuracy
- **12 Health Metrics** including occupation, sleep patterns, vitals
- **Validation Layer** for edge case detection
- **Sleep Score Algorithm** (0-100 scale)

### 📱 Smartwatch Integration
- Simulated Bluetooth connectivity
- Support for Samsung Galaxy Watch, Apple Watch, Fitbit, Garmin
- Auto-sync of heart rate, steps, sleep duration, and quality
- Real-time data synchronization

### 📊 Advanced Visualizations
- **Radar Chart**: Compare patient metrics against healthy baselines
- **Gauge Chart**: Visual risk assessment (0-100)
- **Feature Importance**: ML model interpretability
- **Historical Trends**: Track sleep scores over time

### 🎨 Premium UI/UX
- **Dark Theme**: Professional black aesthetic with cyan accents
- **Responsive Layout**: Optimized for all screen sizes
- **Interactive Charts**: Plotly-powered visualizations
- **Real-time Metrics**: Live health indicators

### 🔬 Clinical Tools
- **What-If Simulator**: Test how lifestyle changes affect sleep health
- **Smart Recommendations**: AI-driven personalized advice
- **Report Generation**: Downloadable clinical reports
- **Historical Tracking**: Session-based analysis history

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Samsung_Capstone_Sleep_Project
```

2. **Create virtual environment** (recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Train the model** (first time only)
```bash
python3 src/train_model.py
```

5. **Run the dashboard**
```bash
streamlit run dashboard/main.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
Samsung_Capstone_Sleep_Project/
├── dashboard/              # Main application
│   ├── main.py            # Streamlit dashboard
│   ├── styles.py          # Dark theme CSS
│   └── utils.py           # Helper functions
├── src/                   # Source code
│   ├── train_model.py     # Model training script
│   └── preprocessing.py   # Data preprocessing
├── models/                # Trained models
│   ├── sleep_model_fast.pkl
│   ├── label_encoder.pkl
│   └── occupation_encoder.pkl
├── data/                  # Dataset
│   └── raw/
│       └── Sleep_health_and_lifestyle_dataset.csv
├── .streamlit/            # Streamlit config
│   └── config.toml
├── requirements.txt       # Python dependencies
└── README.md
```

## 🎮 Usage Guide

### 1. Connect Smartwatch (Optional)
- Select your device from the dropdown
- Click "Connect to Smartwatch"
- Click "Sync Data" to auto-fill health metrics

### 2. Enter Patient Data
- **Demographics**: Gender, Age, Occupation, BMI
- **Sleep & Activity**: Duration, Quality, Activity, Steps
- **Vitals**: Stress, Heart Rate, Blood Pressure

### 3. Run Analysis
- Click "Run Analysis" button
- View diagnosis and risk assessment
- Review personalized recommendations
- Download clinical report

### 4. Explore Features
- **What-If Simulator**: Test lifestyle changes
- **Feature Importance**: See which factors matter most
- **Historical Tracking**: Monitor progress over time

## 🧠 Model Details

### Algorithm
- **Type**: Random Forest Classifier
- **Features**: 12 health metrics
- **Classes**: Healthy, Insomnia, Sleep Apnea
- **Accuracy**: 88%

### Training Data
- **Dataset**: Sleep Health and Lifestyle Dataset
- **Samples**: 374 patient records
- **Features**: Demographics, sleep patterns, vitals, lifestyle

### Validation
- **Test Split**: 20%
- **Cross-validation**: Stratified sampling
- **Edge Case Handling**: Rule-based overrides for extreme values

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **ML Framework**: scikit-learn
- **Visualization**: Plotly
- **Data Processing**: pandas, numpy
- **Styling**: Custom CSS (Dark Theme)

## 📊 Performance Metrics

| Class | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Healthy | 0.95 | 0.98 | 0.97 |
| Insomnia | 0.72 | 0.81 | 0.76 |
| Sleep Apnea | 0.85 | 0.69 | 0.76 |

**Overall Accuracy**: 88%

## 🎨 Theme Customization

The dark theme can be customized in `.streamlit/config.toml`:

```toml
[theme]
base="dark"
primaryColor="#00D9FF"
backgroundColor="#0E1117"
secondaryBackgroundColor="#1A1D24"
textColor="#FAFAFA"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.


## 🙏 Acknowledgments

- Sleep Health and Lifestyle Dataset
- Streamlit community
- scikit-learn documentation

## 🚀 Deployment

This application is deployed on Streamlit Cloud and accessible at:
**[https://ai-sleep-disorder-detection.streamlit.app/](https://ai-sleep-disorder-detection.streamlit.app/)**

### Deploy Your Own Instance

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Deploy using:
   - **Repository**: Your forked repo
   - **Branch**: `main`
   - **Main file**: `dashboard/main.py`

## 📧 Contact

For questions or feedback, please reach out to [chandrilmallick1@gmail.com]

---

**Built with ❤️ for Samsung Capstone Project**
