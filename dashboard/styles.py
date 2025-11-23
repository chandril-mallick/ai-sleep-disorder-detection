def get_css():
    return """
    <style>
    /* Premium Black Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Settings */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #FAFAFA !important;
    }
    
    /* Main Background - Deep Black */
    .stApp {
        background: linear-gradient(135deg, #0E1117 0%, #1A1D24 100%);
    }
    
    /* Sidebar - Slightly Lighter Black */
    [data-testid="stSidebar"] {
        background-color: #1A1D24 !important;
        border-right: 1px solid #2D3139 !important;
    }
    
    /* Headers - Cyan Accent */
    h1, h2, h3, h4, h5, h6 {
        color: #00D9FF !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    h1 {
        border-bottom: 2px solid #00D9FF;
        padding-bottom: 15px;
        margin-bottom: 30px;
        text-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
    }
    
    /* Text Elements */
    p, label, .stMarkdown, .stText, span, div {
        color: #E0E0E0 !important;
    }
    
    /* Buttons - Premium Cyan */
    .stButton > button {
        background: linear-gradient(135deg, #00D9FF 0%, #00A8CC 100%) !important;
        color: #0E1117 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00F0FF 0%, #00C4E0 100%) !important;
        color: #0E1117 !important;
        box-shadow: 0 6px 25px rgba(0, 217, 255, 0.5);
        transform: translateY(-2px);
    }
    
    /* Button Text */
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: #0E1117 !important;
        font-weight: 700 !important;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #2D3139 0%, #1A1D24 100%) !important;
        color: #00D9FF !important;
        border: 2px solid #00D9FF !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #00D9FF 0%, #00A8CC 100%) !important;
        color: #0E1117 !important;
        border-color: #00F0FF !important;
    }
    
    /* Input Fields - Dark with Cyan Accent */
    .stSelectbox div[data-baseweb="select"] > div,
    .stNumberInput div[data-baseweb="input"] > div {
        background-color: #2D3139 !important;
        color: #FAFAFA !important;
        border: 1px solid #3D4149 !important;
        border-radius: 6px !important;
    }
    
    .stNumberInput input {
        background-color: #2D3139 !important;
        color: #FAFAFA !important;
        border: 1px solid #3D4149 !important;
        border-radius: 6px !important;
    }
    
    /* Widget Labels - Bright */
    .stSelectbox label, .stSlider label, .stNumberInput label {
        color: #FAFAFA !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Slider - Cyan Accent */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #00D9FF !important;
    }
    
    .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] > div {
        background-color: #00D9FF !important;
    }
    
    /* Select Dropdown */
    .stSelectbox [data-baseweb="select"] span {
        color: #FAFAFA !important;
    }
    
    /* Expander - Dark Card */
    .streamlit-expanderHeader {
        background-color: #2D3139 !important;
        color: #FAFAFA !important;
        font-weight: 600;
        border-radius: 8px !important;
        border: 1px solid #3D4149 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #1A1D24 !important;
        border: 1px solid #3D4149 !important;
        border-top: none !important;
    }
    
    /* Alert Boxes */
    .stSuccess {
        background-color: #1A3A2A !important;
        color: #4ADE80 !important;
        border-left: 4px solid #4ADE80 !important;
    }
    
    .stError {
        background-color: #3A1A1A !important;
        color: #F87171 !important;
        border-left: 4px solid #F87171 !important;
    }
    
    .stWarning {
        background-color: #3A2A1A !important;
        color: #FBBF24 !important;
        border-left: 4px solid #FBBF24 !important;
    }
    
    .stInfo {
        background-color: #1A2A3A !important;
        color: #00D9FF !important;
        border-left: 4px solid #00D9FF !important;
    }
    
    /* Sidebar Text */
    [data-testid="stSidebar"] * {
        color: #E0E0E0 !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #00D9FF !important;
    }
    
    /* Plotly Charts - Dark Background */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }
    
    /* Markdown Bold */
    strong, b {
        color: #00D9FF !important;
    }
    
    /* Divider */
    hr {
        border-color: #2D3139 !important;
    }
    
    </style>
    """

