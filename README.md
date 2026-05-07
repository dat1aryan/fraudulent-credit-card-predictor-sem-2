# 🔐 Credit Card Fraud Detection - Streamlit App

Enterprise-grade real-time fraud detection system powered by XGBoost machine learning.

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| ROC-AUC | 0.9806 |
| Recall | 77.55% |
| Precision | 88.37% |
| F1-Score | 0.8261 |

## 🚀 Quick Start

### Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## 📦 Project Structure

```
credit-card-fraud-detection/
├── app.py                    # Streamlit application
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
│
└── assets/
    ├── images/              # Visualizations & UI mockups
    └── model/               # Trained model files
        ├── fraud_model.pkl  # XGBoost model
        ├── scaler.pkl       # StandardScaler
        └── model_config.json # Model metadata
```

## 🔧 Technology Stack

- **Framework**: Streamlit
- **ML Model**: XGBoost
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Visualization**: Plotly
- **Serialization**: Joblib

## 🌐 Deploy to Streamlit Cloud

### Step 1: Push to GitHub

```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/credit-card-fraud-detection.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click **"New app"**
3. Connect your GitHub repository
4. Select:
   - **Repository**: `credit-card-fraud-detection`
   - **Branch**: `main`
   - **Main file**: `app.py`
5. Click **"Deploy!"**

Your app will be live at: `https://YOUR_USERNAME-credit-card-fraud-detection.streamlit.app`

## 📝 Features

- ✨ **Real-Time Prediction**: Instant fraud classification
- 📊 **Performance Metrics**: Detailed model statistics
- 📈 **Analytics Dashboard**: Comprehensive model insights
- 🎯 **Interactive UI**: Professional, modern interface
- 🔒 **Production-Ready**: Enterprise-grade reliability

## 🎯 Input Features

The model uses 30 features:
- **Time**: Transaction timestamp
- **Amount**: Transaction value
- **V1-V28**: PCA-transformed features (anonymized)

## 📚 Documentation

- **App**: Built with Streamlit for interactive predictions
- **Model**: Trained on 284,807 transactions with SMOTE balancing
- **Deployment**: Ready for Streamlit Cloud or Docker

## 🔗 Links

- Streamlit Cloud: https://streamlit.io/cloud
- GitHub: https://github.com
- Streamlit Docs: https://docs.streamlit.io

---

**Built with ❤️ for fraud prevention | Ready for production deployment**
