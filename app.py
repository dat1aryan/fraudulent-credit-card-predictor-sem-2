import streamlit as st
import joblib
import numpy as np
import pandas as pd
import json
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Fraud Detection | Enterprise",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
    <style>
    /* Main styling */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5em;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 10px 0 0 0;
        font-size: 1.1em;
        opacity: 0.95;
    }
    
    /* Card styling */
    .card {
        background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
        color: #f8fafc;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.32);
        margin-bottom: 20px;
        border-left: 5px solid #7c3aed;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 14px 38px rgba(15, 23, 42, 0.45);
        transform: translateY(-2px);
    }

    .dark-card {
        background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
        color: #f8fafc;
        border-left: 5px solid #8b5cf6;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.45);
    }

    .dark-card:hover {
        box-shadow: 0 14px 36px rgba(15, 23, 42, 0.6);
    }

    .dark-card .card-title,
    .dark-card p,
    .dark-card strong,
    .dark-card em,
    .dark-card li,
    .dark-card span {
        color: #f8fafc;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.12);
    }

    .card .card-title,
    .card p,
    .card strong,
    .card em,
    .card li,
    .card span {
        color: #f8fafc;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.10);
    }

    .dark-card p {
        line-height: 1.65;
    }
    
    .card-title {
        font-size: 1.3em;
        font-weight: 600;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.12);
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Alert boxes */
    .fraud-alert {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        border-left: 5px solid #ff0000;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .legitimate-alert {
        background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
        color: white;
        border-left: 5px solid #00aa00;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(81, 207, 102, 0.3);
    }
    
    .alert-title {
        font-size: 1.3em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .alert-content {
        font-size: 1em;
        opacity: 0.95;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.14);
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.22);
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.12);
    }
    
    .badge-success {
        background: linear-gradient(135deg, #14532d 0%, #166534 100%);
        color: #ecfdf5;
    }
    
    .badge-danger {
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
        color: #fef2f2;
    }
    
    .badge-info {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
        color: #eff6ff;
    }
    
    /* Input styling */
    .input-section {
        background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
        color: #f8fafc;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 2px solid rgba(124, 58, 237, 0.28);
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.22);
    }

    h2, h3, h4 {
        color: #f8fafc !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.10);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0f172a 0%, #312e81 100%);
        color: #f8fafc;
        border: 1px solid rgba(124, 58, 237, 0.55);
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1em;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.28);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.42);
        border-color: rgba(167, 139, 250, 0.75);
        background: linear-gradient(135deg, #111827 0%, #4338ca 100%);
    }

    .stButton > button:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.25), 0 12px 28px rgba(15, 23, 42, 0.42);
    }
    
    /* Stat row */
    .stat-row {
        display: flex;
        justify-content: space-around;
        gap: 15px;
        margin: 20px 0;
    }
    
    .stat-box {
        flex: 1;
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        color: #f8fafc;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.25);
        border-top: 3px solid #7c3aed;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #0f172a;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        color: #e5e7eb;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #7c3aed 100%);
        color: white;
        box-shadow: 0 0 18px rgba(124, 58, 237, 0.35);
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #0f172a 0%, #172033 100%);
        color: #f8fafc;
        border-left: 4px solid #38bdf8;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.22);
    }
    
    /* Success box */
    .success-box {
        background: linear-gradient(135deg, #0f172a 0%, #13231a 100%);
        color: #f8fafc;
        border-left: 4px solid #22c55e;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.22);
    }
    
    /* Warning box */
    .warning-box {
        background: linear-gradient(135deg, #0f172a 0%, #2a1b0a 100%);
        color: #f8fafc;
        border-left: 4px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.22);
    }

    .info-box h4,
    .success-box h4,
    .warning-box h4,
    .info-box p,
    .success-box p,
    .warning-box p,
    .info-box li,
    .success-box li,
    .warning-box li,
    .info-box strong,
    .success-box strong,
    .warning-box strong {
        color: #f8fafc;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.10);
    }

    .info-box a,
    .success-box a,
    .warning-box a {
        color: #93c5fd;
    }
    
    /* Divider */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(to right, transparent, #667eea, transparent);
        margin: 30px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        color: #cbd5e1;
        font-size: 0.9em;
        border-top: 1px solid rgba(148, 163, 184, 0.18);
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Load model and scaler
@st.cache_resource
def load_artifacts():
    model = joblib.load('assets/model/fraud_model.pkl')
    scaler = joblib.load('assets/model/scaler.pkl')
    with open('assets/model/model_config.json', 'r') as f:
        config = json.load(f)
    return model, scaler, config

try:
    model, scaler, config = load_artifacts()
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.info("Make sure model files are in assets/model/ directory")
    st.stop()

# Sidebar with professional styling
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h2 style='color: #667eea;'>🔐 Fraud Guard</h2>
            <p style='color: #cbd5e1; font-size: 0.9em;'>Enterprise Fraud Detection</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "📊 Real-Time Prediction", "📈 Model Analytics", "⚙️ System Settings"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 15px; border-radius: 10px; margin-top: 30px;'>
            <h4 style='margin-top: 0;'>Model Status</h4>
            <p style='font-size: 0.9em; margin: 5px 0;'><strong>Status:</strong> ✅ Online</p>
            <p style='font-size: 0.9em; margin: 5px 0;'><strong>ROC-AUC:</strong> {:.4f}</p>
            <p style='font-size: 0.9em; margin: 5px 0;'><strong>Predictions:</strong> Real-time</p>
        </div>
    """.format(config['roc_auc']), unsafe_allow_html=True)

# Main content
if page == "🏠 Dashboard":
    # Main header
    st.markdown("""
        <div class='main-header'>
            <h1>🔐 Fraud Detection System</h1>
            <p>Live risk signals for transaction flow</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Key metrics section
    st.markdown("<h2 style='color: #2d3748; margin-bottom: 20px;'>📊 System Performance Overview</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("ROC-AUC Score", f"{config['roc_auc']:.4f}", "0.9806", col1),
        ("Recall Rate", f"{config['recall']:.2%}", "77.55%", col2),
        ("Precision", f"{config['precision']:.2%}", "88.37%", col3),
        ("F1-Score", f"{config['f1_score']:.4f}", "0.8261", col4)
    ]
    
    for label, value, _, col in metrics:
        with col:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value' style='color: #667eea;'>{value}</div>
                    <div class='metric-label'>{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Statistics cards
    st.markdown("<h2 style='color: #2d3748;'>📈 Dataset Statistics</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        ("Total Transactions", "284,807", col1),
        ("Fraudulent Cases", "492", col2),
        ("Fraud Rate", "0.173%", col3),
        ("Features Used", "30", col4)
    ]
    
    for label, value, col in stats:
        with col:
            st.markdown(f"""
                <div class='stat-box'>
                    <h3 style='color: #667eea; margin: 0 0 10px 0;'>{value}</h3>
                    <p style='color: #cbd5e1; margin: 0; font-size: 0.9em;'>{label}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # System features
    st.markdown("<h2 style='color: #2d3748;'>✨ System Capabilities</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='card'>
                <div class='card-title'>⚡ Real-Time Detection</div>
                <p>Live scoring</p>
                <span class='badge badge-success'>Active</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='card'>
                <div class='card-title'>🔍 Advanced Analytics</div>
                <p>Pattern view</p>
                <span class='badge badge-info'>Available</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='card'>
                <div class='card-title'>🛡️ High Accuracy</div>
                <p>High signal</p>
                <span class='badge badge-success'>Verified</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Model information
    st.markdown("<h2 style='color: #2d3748;'>🤖 Model Information</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class='card'>
                <div class='card-title'>Algorithm & Configuration</div>
                <p><strong>Model:</strong> {config['model_name']}</p>
                <p><strong>Threshold:</strong> {config['optimal_threshold']:.4f}</p>
                <p><strong>Pipeline:</strong> SMOTE + tuning</p>
                <p><strong>Status:</strong> Ready</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card'>
                <div class='card-title'>Performance Metrics</div>
                <p><strong>Recall:</strong> {config['recall']:.2%}</p>
                <p><strong>Precision:</strong> {config['precision']:.2%}</p>
                <p><strong>ROC-AUC:</strong> {config['roc_auc']:.4f}</p>
                <p><strong>Mode:</strong> Production</p>
            </div>
        """, unsafe_allow_html=True)

elif page == "📊 Real-Time Prediction":
    st.markdown("""
        <div class='main-header'>
            <h1>📊 Real-Time Fraud Detection</h1>
            <p>Compact signal view</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #2d3748;'>💳 Transaction Details</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("<h4 style='color: #667eea;'>Transaction Amount</h4>", unsafe_allow_html=True)
            amount = st.number_input(
                "Amount (USD)",
                min_value=0.0,
                max_value=25691.16,
                value=100.0,
                step=0.01,
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("<h4 style='color: #667eea;'>Transaction Time</h4>", unsafe_allow_html=True)
            time = st.number_input(
                "Time (seconds)",
                min_value=0,
                max_value=172792,
                value=0,
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown("<h4 style='color: #667eea;'>Sample Data</h4>", unsafe_allow_html=True)
            use_sample = st.checkbox("Use Demo Features", value=True, help="Auto-populate PCA features")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #2d3748;'>🔧 Feature Configuration</h2>", unsafe_allow_html=True)
    
    with st.expander("📋 PCA Components (V1-V28)", expanded=False):
        if use_sample:
            st.info("✨ Using pre-configured sample features for demonstration")
            features = np.random.randn(28) * 0.5
        else:
            st.write("Enter individual PCA component values (normalized between -3 and 3):")
            features = []
            feature_cols = st.columns(4)
            for i in range(28):
                with feature_cols[i % 4]:
                    v = st.number_input(
                        f"V{i+1}",
                        value=0.0,
                        min_value=-5.0,
                        max_value=5.0,
                        key=f"v{i}"
                    )
                    features.append(v)
            features = np.array(features)
    
    # Prediction button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        predict_clicked = st.button(
            "🔍 ANALYZE TRANSACTION",
            use_container_width=True,
            type="primary"
        )
    
    if predict_clicked:
        with st.spinner("🔄 Processing transaction..."):
            try:
                # Prepare input
                input_data = np.concatenate([[time, amount], features]).reshape(1, -1)
                input_scaled = scaler.transform(input_data)
                
                # Make prediction
                y_pred_proba = model.predict_proba(input_scaled)[0]
                fraud_prob = y_pred_proba[1]
                legit_prob = y_pred_proba[0]
                threshold = config['optimal_threshold']
                
                # Determine prediction
                is_fraud = fraud_prob >= threshold
                
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<h2 style='color: #2d3748;'>🎯 Analysis Result</h2>", unsafe_allow_html=True)
                
                # Result display
                if is_fraud:
                    st.markdown(f"""
                        <div class='fraud-alert'>
                            <div class='alert-title'>⚠️ FRAUDULENT TRANSACTION DETECTED</div>
                            <div class='alert-content'>
                                This transaction has been flagged as suspicious and requires immediate review.
                                <br><br>
                                <strong>Risk Score: {fraud_prob:.2%}</strong>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class='legitimate-alert'>
                            <div class='alert-title'>✓ LEGITIMATE TRANSACTION</div>
                            <div class='alert-content'>
                                This transaction appears to be legitimate and safe to process.
                                <br><br>
                                <strong>Confidence Score: {legit_prob:.2%}</strong>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Detailed metrics
                st.markdown("<h3 style='color: #2d3748; margin-top: 30px;'>📊 Prediction Metrics</h3>", unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-value' style='color: #ff6b6b;'>{fraud_prob:.2%}</div>
                            <div class='metric-label'>Fraud Probability</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-value' style='color: #51cf66;'>{legit_prob:.2%}</div>
                            <div class='metric-label'>Legitimate Probability</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-value' style='color: #667eea;'>${amount:.2f}</div>
                            <div class='metric-label'>Amount</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    status_badge = "🚨 Flagged" if is_fraud else "✅ Clear"
                    status_color = "#ff6b6b" if is_fraud else "#51cf66"
                    st.markdown(f"""
                        <div class='metric-card' style='background: {status_color}; color: white;'>
                            <div class='metric-value'>{status_badge}</div>
                            <div class='metric-label'>Status</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Probability gauge
                st.markdown("<h3 style='color: #2d3748; margin-top: 30px;'>📈 Risk Gauge</h3>", unsafe_allow_html=True)
                
                # Create gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=fraud_prob * 100,
                    title={'text': "Fraud Risk Score"},
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#667eea"},
                        'steps': [
                            {'range': [0, 30], 'color': "#51cf66"},
                            {'range': [30, 70], 'color': "#ffd43b"},
                            {'range': [70, 100], 'color': "#ff6b6b"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': threshold * 100
                        }
                    }
                ))
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Transaction summary
                st.markdown("<h3 style='color: #2d3748; margin-top: 30px;'>📝 Transaction Summary</h3>", unsafe_allow_html=True)
                
                summary_df = pd.DataFrame({
                    'Parameter': ['Transaction Amount', 'Time (Seconds)', 'Fraud Probability', 'Status', 'Action'],
                    'Value': [f'${amount:.2f}', str(time), f'{fraud_prob:.2%}', 
                             '🚨 Review' if is_fraud else '✅ Approve', 
                             'Requires Review' if is_fraud else 'Safe to Process']
                })
                
                st.dataframe(summary_df, use_container_width=True, hide_index=True)
                
            except Exception as e:
                st.error(f"❌ Analysis error: {e}")
                st.info("Please check your input values and try again")

elif page == "📈 Model Analytics":
    st.markdown("""
        <div class='main-header'>
            <h1>📈 Model Analytics & Insights</h1>
            <p>Compact performance view</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Performance Overview
    st.markdown("<h2 style='color: #2d3748;'>🎯 Performance Overview</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = [
        ("ROC-AUC", config['roc_auc'], "#667eea", col1),
        ("Recall", config['recall'], "#51cf66", col2),
        ("Precision", config['precision'], "#ffd43b", col3),
        ("F1-Score", config['f1_score'], "#ff6b6b", col4),
    ]
    
    for label, value, color, col in metrics_data:
        with col:
            st.markdown(f"""
                <div class='metric-card' style='background: linear-gradient(135deg, {color} 0%, {color}cc 100%);'>
                    <div class='metric-value'>{value:.4f}</div>
                    <div class='metric-label'>{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Performance Visualizations
    st.markdown("<h2 style='color: #2d3748;'>📊 Performance Visualization</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance comparison chart
        performance_data = {
            'Metric': ['Recall', 'Precision', 'F1-Score', 'ROC-AUC'],
            'Score': [config['recall'], config['precision'], config['f1_score'], config['roc_auc']]
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=performance_data['Metric'],
                y=performance_data['Score'],
                marker=dict(
                    color=['#51cf66', '#ffd43b', '#ff6b6b', '#667eea'],
                    line=dict(color='white', width=2)
                ),
                text=[f"{val:.2%}" if val < 1 else f"{val:.4f}" for val in performance_data['Score']],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Model Performance Metrics",
            yaxis_title="Score",
            xaxis_title="Metric",
            height=400,
            showlegend=False,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # ROC-AUC gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=config['roc_auc'] * 100,
            title={'text': "Overall ROC-AUC Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 50], 'color': "#f8f9fa"},
                    {'range': [50, 80], 'color': "#fff3bf"},
                    {'range': [80, 100], 'color': "#d3f9d8"}
                ],
                'threshold': {
                    'line': {'color': "darkblue", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Model Configuration
    st.markdown("<h2 style='color: #2d3748;'>⚙️ Model Configuration</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='card'>
                <div class='card-title'>🤖 Algorithm</div>
                <p><strong>{config['model_name']}</strong></p>
                <p style='color: #cbd5e1; font-size: 0.9em;'>Gradient boosting</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card'>
                <div class='card-title'>🎯 Decision Threshold</div>
                <p><strong>{config['optimal_threshold']:.4f}</strong></p>
                <p style='color: #cbd5e1; font-size: 0.9em;'>Decision boundary</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='card'>
                <div class='card-title'>📊 Input Features</div>
                <p><strong>{config['n_features']} Features</strong></p>
                <p style='color: #cbd5e1; font-size: 0.9em;'>Time + Amount + PCA</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Feature Details
    st.markdown("<h2 style='color: #2d3748;'>📋 Feature Specification</h2>", unsafe_allow_html=True)
    
    with st.expander("🔍 Detailed Feature Information", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class='card'>
                    <div class='card-title'>⏱️ Temporal Feature</div>
                    <p><strong>Time</strong></p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>Sequence signal</p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>0 - 172,792 sec</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='card'>
                    <div class='card-title'>💰 Transaction Feature</div>
                    <p><strong>Amount</strong></p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>Value signal</p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>$0 - $25,691.16</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class='card dark-card' style='margin-top: 20px;'>
                <div class='card-title'>🔐 PCA Components (V1-V28)</div>
                <p><strong>V1-V28</strong></p>
                <p style='color: #cbd5e1; font-size: 0.9em;'>Abstract feature layer</p>
                <p style='color: #cbd5e1; font-size: 0.9em;'>Privacy-preserving signal</p>
                <p style='color: #cbd5e1; margin-top: 15px;'><em>Note: V1-V28 are anonymized due to confidentiality agreements</em></p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Dataset Statistics
    st.markdown("<h2 style='color: #2d3748;'>📊 Training Dataset Statistics</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='stat-box'>
                <h3 style='color: #667eea; margin: 0 0 10px 0;'>284,807</h3>
                <p style='color: #cbd5e1; margin: 0; font-size: 0.9em;'>Total Transactions</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='stat-box'>
                <h3 style='color: #51cf66; margin: 0 0 10px 0;'>284,315</h3>
                <p style='color: #cbd5e1; margin: 0; font-size: 0.9em;'>Legitimate Cases</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='stat-box'>
                <h3 style='color: #ff6b6b; margin: 0 0 10px 0;'>492</h3>
                <p style='color: #cbd5e1; margin: 0; font-size: 0.9em;'>Fraudulent Cases</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='stat-box'>
                <h3 style='color: #ffd43b; margin: 0 0 10px 0;'>0.173%</h3>
                <p style='color: #cbd5e1; margin: 0; font-size: 0.9em;'>Class Imbalance Ratio</p>
            </div>
        """, unsafe_allow_html=True)

elif page == "⚙️ System Settings":
    st.markdown("""
        <div class='main-header'>
            <h1>⚙️ System Configuration</h1>
            <p>Model parameters, settings, and system information</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Configuration Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 Model Config", "📊 Metrics", "🔧 Advanced", "ℹ️ System Info"])
    
    with tab1:
        st.markdown("<h2 style='color: #2d3748;'>Model Configuration</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div class='card'>
                    <div class='card-title'>🎯 Core Parameters</div>
                    <p><strong>{config['model_name']}</strong></p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>Binary classifier</p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>Tuned pipeline</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='card'>
                    <div class='card-title'>🎚️ Decision Boundary</div>
                    <p><strong>Optimal Threshold:</strong> <span style='color: #667eea; font-weight: bold;'>{config['optimal_threshold']:.4f}</span></p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>Boundary tuning</p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>Below: legit | Above: fraud</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Threshold adjustment info
        st.info("""
        ⚠️ **Note:** The current threshold is optimized for production use. Adjusting this value 
        affects the model's behavior:
        - **Lower threshold** → More fraud detections, but more false positives
        - **Higher threshold** → Fewer false positives, but more fraud may slip through
        """)
    
    with tab2:
        st.markdown("<h2 style='color: #2d3748;'>Performance Metrics</h2>", unsafe_allow_html=True)
        
        # Create metrics dataframe
        metrics_df = pd.DataFrame({
            'Metric': ['ROC-AUC Score', 'Recall (Sensitivity)', 'Precision (Specificity)', 'F1-Score'],
            'Value': [
                f"{config['roc_auc']:.4f}",
                f"{config['recall']:.4f}",
                f"{config['precision']:.4f}",
                f"{config['f1_score']:.4f}"
            ],
            'Percentage': [
                f"{config['roc_auc']*100:.2f}%",
                f"{config['recall']*100:.2f}%",
                f"{config['precision']*100:.2f}%",
                f"{config['f1_score']*100:.2f}%"
            ],
            'Interpretation': [
                'Overall discriminative ability',
                'Fraud detection rate',
                'Accuracy of fraud alerts',
                'Harmonic mean of precision & recall'
            ]
        })
        
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Detailed interpretation
        st.markdown("""
            <div class='info-box'>
                <h4>📖 Metric Snapshot</h4>
                <ul>
                    <li><strong>ROC-AUC:</strong> 0.9806</li>
                    <li><strong>Recall:</strong> 77.55%</li>
                    <li><strong>Precision:</strong> 88.37%</li>
                    <li><strong>F1-Score:</strong> 0.8261</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<h2 style='color: #2d3748;'>Advanced Settings</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class='card'>
                    <div class='card-title'>🔬 Training Configuration</div>
                    <p><strong>227,846</strong></p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>Balanced train set</p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>SMOTE + scaling</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='card'>
                    <div class='card-title'>⚙️ Model Tuning</div>
                    <p><strong>RandomizedSearchCV</strong></p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>10 trials</p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>ROC-AUC objective</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Feature preprocessing
        st.markdown("""
            <div class='success-box'>
                <h4>📋 Data Preprocessing Pipeline</h4>
                <ol>
                    <li>Train-Test Split (80-20, stratified)</li>
                    <li>StandardScaler normalization</li>
                    <li>SMOTE on training data</li>
                    <li>Model fit</li>
                    <li>Test on original split</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("<h2 style='color: #2d3748;'>System Information</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div class='card'>
                    <div class='card-title'>📦 Model Artifacts</div>
                    <p><strong>fraud_model.pkl</strong></p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>scaler.pkl + config</p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>~242 KB total</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='card'>
                    <div class='card-title'>🌐 Deployment Info</div>
                    <p><strong>Streamlit</strong></p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>Python 3.13</p>
                    <p style='color: #cbd5e1; font-size: 0.9em;'>Production ready</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # System specifications
        st.markdown("""
            <div class='warning-box'>
                <h4>🔧 System Requirements</h4>
                <ul>
                    <li><strong>Python:</strong> 3.8+</li>
                    <li><strong>Packages:</strong> streamlit, xgboost, joblib</li>
                    <li><strong>Memory:</strong> ~50 MB</li>
                    <li><strong>Latency:</strong> <5ms</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# Professional Footer
st.markdown("""
    <hr>
    <div class='footer'>
        <div style='display: flex; justify-content: center; gap: 30px; margin-bottom: 15px;'>
            <div>
                <strong>Model:</strong> {}<br>
                <strong>Algorithm:</strong> XGBoost
            </div>
            <div>
                <strong>Performance:</strong> ROC-AUC {:.4f}<br>
                <strong>Status:</strong> ✅ Online
            </div>
            <div>
                <strong>Updated:</strong> 2026-05-07<br>
                <strong>Version:</strong> 1.0.0
            </div>
        </div>
        <p style='margin-top: 20px; font-size: 0.85em; color: #cbd5e1;'>
            © 2026 Fraud Detection System | Enterprise-Grade Real-Time Protection | 
            <strong>Protecting transactions. Preventing fraud. Building trust.</strong>
        </p>
        <p style='font-size: 0.8em; color: #ccc;'>
            Developed with machine learning | Deployed with Streamlit | Secured with industry standards
        </p>
    </div>
""".format(config['model_name'], config['roc_auc']), unsafe_allow_html=True)
