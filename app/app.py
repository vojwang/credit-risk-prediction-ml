import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("../models/credit_risk_random_forest.pkl")

# Load saved encoders
encoders = joblib.load("../models/label_encoders.pkl")

# Page Configuration
st.set_page_config(
    page_title="Credit Risk Prediction",
    page_icon="🏦",
    layout="centered"
)

# Application Title
st.title("🏦 Credit Risk Prediction System")

# Introduction
st.write("""
This application uses a **Random Forest Machine Learning Model**
to predict whether a customer is likely to be a **Good** or **Bad**
credit risk.
""")

# Customer Information
st.header("Customer Information")

# Age
age = st.number_input(
    "Age",
    min_value=18,
    max_value=75,
    value=30
)

# Sex
sex = st.selectbox(
    "Sex",
    ["male", "female"]
)

# Job
job = st.selectbox(
    "Job",
    [0, 1, 2, 3]
)

# Housing
housing = st.selectbox(
    "Housing",
    ["own", "rent", "free"]
)

# Saving Accounts
saving_accounts = st.selectbox(
    "Saving Accounts",
    ["little", "moderate", "quite rich", "rich"]
)

# Checking Account
checking_account = st.selectbox(
    "Checking Account",
    ["little", "moderate", "rich"]
)

# Credit Amount
credit_amount = st.number_input(
    "Credit Amount",
    min_value=250,
    max_value=20000,
    value=2000
)

# Loan Duration
duration = st.number_input(
    "Loan Duration (Months)",
    min_value=4,
    max_value=72,
    value=12
)

# Loan Purpose
purpose = st.selectbox(
    "Purpose",
    [
        "business",
        "car",
        "domestic appliances",
        "education",
        "furniture/equipment",
        "radio/TV",
        "repairs",
        "vacation/others"
    ]
)

# Predict Button
predict_button = st.button("Predict Credit Risk")

if predict_button:

    # Encode categorical variables
    sex_encoded = encoders["Sex"].transform([sex])[0]
    housing_encoded = encoders["Housing"].transform([housing])[0]
    saving_encoded = encoders["Saving accounts"].transform([saving_accounts])[0]
    checking_encoded = encoders["Checking account"].transform([checking_account])[0]
    purpose_encoded = encoders["Purpose"].transform([purpose])[0]

    # Create input DataFrame
    input_data = pd.DataFrame({
        "Age": [age],
        "Sex": [sex_encoded],
        "Job": [job],
        "Housing": [housing_encoded],
        "Saving accounts": [saving_encoded],
        "Checking account": [checking_encoded],
        "Credit amount": [credit_amount],
        "Duration": [duration],
        "Purpose": [purpose_encoded]
    })

    # Make prediction
    prediction = model.predict(input_data)

    # Prediction probabilities
    probability = model.predict_proba(input_data)

    # Convert prediction back to original label
    prediction_label = encoders["Risk"].inverse_transform(prediction)[0]

    # Display prediction
    st.subheader("Prediction Result")

    if prediction_label == "good":
        st.success("✅ Good Credit Risk")
    else:
        st.error("❌ Bad Credit Risk")

    # Display probabilities
    good_index = encoders["Risk"].transform(["good"])[0]
    bad_index = encoders["Risk"].transform(["bad"])[0]

    good_prob = probability[0][good_index] * 100
    bad_prob = probability[0][bad_index] * 100

    st.subheader("Prediction Probabilities")
    st.write(f"✅ Good Credit Risk: **{good_prob:.2f}%**")
    st.write(f"❌ Bad Credit Risk: **{bad_prob:.2f}%**")