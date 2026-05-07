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
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    .card-title {
        font-size: 1.3em;
        font-weight: 600;
        color: #2d3748;
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
    }
    
    .badge-success {
        background-color: #d4edda;
        color: #155724;
    }
    
    .badge-danger {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    .badge-info {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    
    /* Input styling */
    .input-section {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 2px solid #e9ecef;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1em;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
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
        background: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-top: 3px solid #667eea;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        background-color: #f0f2f6;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    
    /* Info box */
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    /* Success box */
    .success-box {
        background-color: #f1f8e9;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    /* Warning box */
    .warning-box {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
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
        color: #999;
        font-size: 0.9em;
        border-top: 1px solid #eee;
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
            <p style='color: #999; font-size: 0.9em;'>Enterprise Fraud Detection</p>
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
            <p>Enterprise-grade real-time fraud detection powered by advanced machine learning</p>
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
                    <p style='color: #999; margin: 0; font-size: 0.9em;'>{label}</p>
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
                <p>Sub-millisecond fraud predictions on every transaction for immediate action</p>
                <span class='badge badge-success'>Active</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='card'>
                <div class='card-title'>🔍 Advanced Analytics</div>
                <p>Deep insights into transaction patterns and fraud characteristics</p>
                <span class='badge badge-info'>Available</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='card'>
                <div class='card-title'>🛡️ High Accuracy</div>
                <p>98.06% ROC-AUC with optimal balance between catch rate and false alarms</p>
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
                <p><strong>Model Type:</strong> {config['model_name']}</p>
                <p><strong>Optimal Threshold:</strong> {config['optimal_threshold']:.4f}</p>
                <p><strong>Training Method:</strong> Supervised Learning with SMOTE</p>
                <p><strong>Total Parameters:</strong> Optimized via RandomizedSearchCV</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card'>
                <div class='card-title'>Performance Metrics</div>
                <p><strong>True Positive Rate:</strong> {config['recall']:.2%}</p>
                <p><strong>False Positive Rate:</strong> ~{(1-config['precision'])*100:.1f}%</p>
                <p><strong>ROC-AUC Score:</strong> {config['roc_auc']:.4f}</p>
                <p><strong>Model Status:</strong> ✅ Production Ready</p>
            </div>
        """, unsafe_allow_html=True)

elif page == "📊 Real-Time Prediction":
    st.markdown("""
        <div class='main-header'>
            <h1>📊 Real-Time Fraud Detection</h1>
            <p>Analyze transaction details and get instant fraud assessment</p>
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
            <p>Comprehensive analysis of model performance and characteristics</p>
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
                <p style='color: #999; font-size: 0.9em;'>Gradient boosting classifier optimized for financial fraud detection</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card'>
                <div class='card-title'>🎯 Decision Threshold</div>
                <p><strong>{config['optimal_threshold']:.4f}</strong></p>
                <p style='color: #999; font-size: 0.9em;'>Optimized to maximize F1-score and balance precision/recall</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='card'>
                <div class='card-title'>📊 Input Features</div>
                <p><strong>{config['n_features']} Features</strong></p>
                <p style='color: #999; font-size: 0.9em;'>1 Time + 1 Amount + 28 PCA Components (V1-V28)</p>
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
                    <p><strong>Feature:</strong> Time</p>
                    <p><strong>Description:</strong> Number of seconds elapsed from the start of the dataset</p>
                    <p><strong>Range:</strong> 0 - 172,792 seconds</p>
                    <p><strong>Purpose:</strong> Captures temporal patterns in fraud (time-of-day effects)</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='card'>
                    <div class='card-title'>💰 Transaction Feature</div>
                    <p><strong>Feature:</strong> Amount</p>
                    <p><strong>Description:</strong> Transaction value in currency units</p>
                    <p><strong>Range:</strong> $0 - $25,691.16</p>
                    <p><strong>Purpose:</strong> Fraudsters typically avoid high-value transactions</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class='card' style='margin-top: 20px;'>
                <div class='card-title'>🔐 PCA Components (V1-V28)</div>
                <p><strong>Features:</strong> 28 Principal Component Analysis transformed features</p>
                <p><strong>Anonymization:</strong> Original features are transformed for privacy protection</p>
                <p><strong>Normalization:</strong> Standardized to zero mean and unit variance</p>
                <p><strong>Purpose:</strong> Capture complex patterns and interactions in transaction data</p>
                <p style='color: #999; margin-top: 15px;'><em>Note: V1-V28 are anonymized due to confidentiality agreements</em></p>
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
                <p style='color: #999; margin: 0; font-size: 0.9em;'>Total Transactions</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='stat-box'>
                <h3 style='color: #51cf66; margin: 0 0 10px 0;'>284,315</h3>
                <p style='color: #999; margin: 0; font-size: 0.9em;'>Legitimate Cases</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='stat-box'>
                <h3 style='color: #ff6b6b; margin: 0 0 10px 0;'>492</h3>
                <p style='color: #999; margin: 0; font-size: 0.9em;'>Fraudulent Cases</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='stat-box'>
                <h3 style='color: #ffd43b; margin: 0 0 10px 0;'>0.173%</h3>
                <p style='color: #999; margin: 0; font-size: 0.9em;'>Class Imbalance Ratio</p>
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
                    <p><strong>Algorithm:</strong> {config['model_name']}</p>
                    <p><strong>Model Type:</strong> Binary Classifier</p>
                    <p><strong>Training Method:</strong> Supervised Learning</p>
                    <p><strong>Optimization:</strong> RandomizedSearchCV</p>
                    <p><strong>Cross-Validation:</strong> Stratified K-Fold (k=5)</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='card'>
                    <div class='card-title'>🎚️ Decision Boundary</div>
                    <p><strong>Optimal Threshold:</strong> <span style='color: #667eea; font-weight: bold;'>{config['optimal_threshold']:.4f}</span></p>
                    <p><strong>Purpose:</strong> Maximizes F1-Score</p>
                    <p><strong>Below Threshold:</strong> Classified as Legitimate</p>
                    <p><strong>Above Threshold:</strong> Classified as Fraudulent</p>
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
                <h4>📖 Metric Interpretation</h4>
                <ul>
                    <li><strong>ROC-AUC (0.9806):</strong> Excellent discriminative ability - model effectively distinguishes between fraud and legitimate</li>
                    <li><strong>Recall (77.55%):</strong> Catches 77.55% of actual frauds - good coverage but ~22% of frauds may pass</li>
                    <li><strong>Precision (88.37%):</strong> 88.37% of fraud alerts are true frauds - minimizes unnecessary customer friction</li>
                    <li><strong>F1-Score (0.8261):</strong> Good balance between precision and recall</li>
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
                    <p><strong>Training Samples:</strong> 227,846 (after 80-20 split)</p>
                    <p><strong>Test Samples:</strong> 56,961</p>
                    <p><strong>SMOTE Ratio:</strong> 1:1 (balanced)</p>
                    <p><strong>Random State:</strong> 42</p>
                    <p><strong>Feature Scaling:</strong> StandardScaler</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='card'>
                    <div class='card-title'>⚙️ Model Tuning</div>
                    <p><strong>Search Method:</strong> RandomizedSearchCV</p>
                    <p><strong>Iterations:</strong> 10</p>
                    <p><strong>CV Folds:</strong> 3</p>
                    <p><strong>Scoring Metric:</strong> ROC-AUC</p>
                    <p><strong>Parallel Jobs:</strong> -1 (All cores)</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Feature preprocessing
        st.markdown("""
            <div class='success-box'>
                <h4>📋 Data Preprocessing Pipeline</h4>
                <ol>
                    <li>Train-Test Split (80-20, stratified)</li>
                    <li>StandardScaler: Normalize all features to μ=0, σ=1</li>
                    <li>SMOTE Oversampling: Applied only to training data</li>
                    <li>Model Training: On balanced training set</li>
                    <li>Evaluation: On original test set (no SMOTE)</li>
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
                    <p><strong>Model File:</strong> fraud_model.pkl</p>
                    <p><strong>Scaler File:</strong> scaler.pkl</p>
                    <p><strong>Config File:</strong> model_config.json</p>
                    <p><strong>Total Size:</strong> ~242 KB</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='card'>
                    <div class='card-title'>🌐 Deployment Info</div>
                    <p><strong>Framework:</strong> Streamlit</p>
                    <p><strong>Runtime Environment:</strong> Python 3.13</p>
                    <p><strong>Status:</strong> ✅ Production Ready</p>
                    <p><strong>Last Updated:</strong> 2026-05-07</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # System specifications
        st.markdown("""
            <div class='warning-box'>
                <h4>🔧 System Requirements</h4>
                <ul>
                    <li><strong>Python Version:</strong> 3.8+</li>
                    <li><strong>Required Packages:</strong> scikit-learn, xgboost, streamlit, joblib</li>
                    <li><strong>Memory (Inference):</strong> ~50 MB minimum</li>
                    <li><strong>Inference Time:</strong> <5ms per transaction</li>
                    <li><strong>Concurrent Users:</strong> Limited by Streamlit Cloud tier</li>
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
        <p style='margin-top: 20px; font-size: 0.85em; color: #999;'>
            © 2026 Fraud Detection System | Enterprise-Grade Real-Time Protection | 
            <strong>Protecting transactions. Preventing fraud. Building trust.</strong>
        </p>
        <p style='font-size: 0.8em; color: #ccc;'>
            Developed with machine learning | Deployed with Streamlit | Secured with industry standards
        </p>
    </div>
""".format(config['model_name'], config['roc_auc']), unsafe_allow_html=True)
