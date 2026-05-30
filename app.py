import streamlit as st
import pickle
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Telecom Churn Prediction",
    page_icon="📊",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------
model = pickle.load(open('churn_model.pkl', 'rb'))
model_columns = pickle.load(open('model_columns.pkl', 'rb'))

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>

    .main {
        background-color: #f5f7fa;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: #1f77b4;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 30px;
    }

    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 18px;
        border-radius: 12px;
        height: 50px;
        border: none;
    }

    .stButton>button:hover {
        background-color: #125a96;
    }

    </style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    '<div class="title">📊 Telecom Customer Churn Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Machine Learning Based Customer Retention System</div>',
    unsafe_allow_html=True
)

# ---------------- INPUT SECTION ----------------
st.subheader("📌 Customer Information")

col1, col2 = st.columns(2)

with col1:

    tenure = st.number_input(
        "Tenure (Months)",
        min_value=0,
        max_value=100,
        value=12
    )

    monthlycharges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        max_value=500.0,
        value=70.0
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    senior = st.selectbox(
        "Senior Citizen",
        ["No", "Yes"]
    )

    partner = st.selectbox(
        "Partner",
        ["No", "Yes"]
    )

with col2:

    dependents = st.selectbox(
        "Dependents",
        ["No", "Yes"]
    )

    internet = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    contract = st.selectbox(
        "Contract Type",
        ["Month-to-month", "One year", "Two year"]
    )

    techsupport = st.selectbox(
        "Tech Support",
        ["No", "Yes"]
    )

    payment = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

# ---------------- AUTO TOTAL CHARGES ----------------
totalcharges = tenure * monthlycharges

st.info(f"💰 Total Charges: {totalcharges:.2f}")

# ---------------- PREDICTION ----------------
if st.button("🔍 Predict Churn"):

    # Create dataframe
    input_data = pd.DataFrame(columns=model_columns)

    input_data.loc[0] = 0

    # Numerical Features
    if 'tenure' in input_data.columns:
        input_data.at[0, 'tenure'] = tenure

    if 'MonthlyCharges' in input_data.columns:
        input_data.at[0, 'MonthlyCharges'] = monthlycharges

    if 'TotalCharges' in input_data.columns:
        input_data.at[0, 'TotalCharges'] = totalcharges

    # Gender
    if 'gender_Male' in input_data.columns:
        input_data.at[0, 'gender_Male'] = 1 if gender == "Male" else 0

    # Senior Citizen
    if 'SeniorCitizen' in input_data.columns:
        input_data.at[0, 'SeniorCitizen'] = 1 if senior == "Yes" else 0

    # Partner
    if 'Partner_Yes' in input_data.columns:
        input_data.at[0, 'Partner_Yes'] = 1 if partner == "Yes" else 0

    # Dependents
    if 'Dependents_Yes' in input_data.columns:
        input_data.at[0, 'Dependents_Yes'] = 1 if dependents == "Yes" else 0

    # Internet Service
    if 'InternetService_Fiber optic' in input_data.columns:
        input_data.at[0, 'InternetService_Fiber optic'] = 1 if internet == "Fiber optic" else 0

    if 'InternetService_No' in input_data.columns:
        input_data.at[0, 'InternetService_No'] = 1 if internet == "No" else 0

    # Contract Type
    if 'Contract_One year' in input_data.columns:
        input_data.at[0, 'Contract_One year'] = 1 if contract == "One year" else 0

    if 'Contract_Two year' in input_data.columns:
        input_data.at[0, 'Contract_Two year'] = 1 if contract == "Two year" else 0

    # Tech Support
    if 'TechSupport_Yes' in input_data.columns:
        input_data.at[0, 'TechSupport_Yes'] = 1 if techsupport == "Yes" else 0

    # Payment Method
    if 'PaymentMethod_Credit card (automatic)' in input_data.columns:
        input_data.at[0, 'PaymentMethod_Credit card (automatic)'] = 1 if payment == "Credit card (automatic)" else 0

    if 'PaymentMethod_Electronic check' in input_data.columns:
        input_data.at[0, 'PaymentMethod_Electronic check'] = 1 if payment == "Electronic check" else 0

    if 'PaymentMethod_Mailed check' in input_data.columns:
        input_data.at[0, 'PaymentMethod_Mailed check'] = 1 if payment == "Mailed check" else 0

    # ---------------- PREDICT ----------------
    prediction = model.predict(input_data)

    probability = model.predict_proba(input_data)[0][1]

    st.markdown("---")

    # ---------------- OUTPUT ----------------
    if prediction[0] == 1:

        st.error(
            f"""
            ⚠️ Customer is likely to CHURN

            Churn Probability: {probability*100:.2f}%
            """
        )

    else:

        st.success(
            f"""
            ✅ Customer is likely to STAY

            Churn Probability: {probability*100:.2f}%
            """
        )

# ---------------- FOOTER ----------------
st.markdown("---")

st.caption(
    "Developed using Streamlit, Tableau, Python & Machine Learning"
)