import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Specific Health Guidance App", page_icon="🇯🇵", layout="centered")

# --- Title and Description ---
st.title("Specific Health Guidance Stratification App")

# Explanation of the Japanese system (Context for global audience)
st.markdown("""
This tool automates the stratification logic for **Specific Health Guidance (Tokutei Hoken Shido)**, a national health screening program in Japan.

Designed by the **Ministry of Health, Labour and Welfare**, this system aims to prevent lifestyle-related diseases by identifying **Metabolic Syndrome risks**. 
Based on the input data, individuals are categorized into three levels of support:

- 🔴 **Active Support**: High risk (Requires intensive intervention)
- 🟡 **Motivational Support**: Moderate risk (Requires lifestyle advice)
- 🟢 **Information Provision**: Low risk
""")

st.divider()

# --- Input Form ---
st.header("📝 Input Form")

# 1. Basic Information
st.subheader("1. Basic Information")

col1, col2 = st.columns(2)
with col1:
    gender_option = st.radio("Gender", ["Male", "Female"], horizontal=True)
with col2:
    # Default age set to 40 (start age for Specific Health Guidance)
    age = st.number_input("Age", min_value=0, value=40)

# Input for Waist and BMI
waist = st.number_input("Waist Circumference (cm)", min_value=0.0, step=0.1)
bmi = st.number_input("BMI", min_value=0.0, step=0.1)

# Convert gender to system value ("1" or "2")
gender = "1" if gender_option == "Male" else "2"


# 2. Test Values (Risk Assessment)
st.subheader("2. Clinical Test Values")
st.caption("※ Leave as 0 if the value is within the standard range or unknown.")

# Glucose
st.markdown("##### 🩸 Glucose")
c_bs, c_a1c = st.columns(2)
with c_bs:
    bs = st.number_input("Fasting Plasma Glucose (mg/dl)", min_value=0.0)
with c_a1c:
    hba1c = st.number_input("HbA1c (%)", min_value=0.0, step=0.1)

# Lipids
st.markdown("##### 🍔 Lipids")
c_tg, c_hdl = st.columns(2)
with c_tg:
    tg = st.number_input("Triglycerides (mg/dl)", min_value=0.0)
with c_hdl:
    hdl = st.number_input("HDL Cholesterol (mg/dl)", min_value=0.0)

# Blood Pressure
st.markdown("##### 💓 Blood Pressure")
c_sys, c_dia = st.columns(2)
with c_sys:
    bp_sys = st.number_input("Systolic BP (mmHg)", min_value=0.0)
with c_dia:
    bp_dia = st.number_input("Diastolic BP (mmHg)", min_value=0.0)

# 3. Lifestyle Habits
st.subheader("3. Lifestyle Habits")
smoke_option = st.radio("Do you smoke?", ["No", "Yes"], horizontal=True)
smoke_flg = True if smoke_option == "Yes" else False


# --- Judgment Button ---
st.divider()

if st.button("Run Assessment 🚀", type="primary", use_container_width=True):
    
    st.markdown("### 📊 Assessment Results")

    # === Logic Start ===
    
    # 1. Visceral Fat Obesity Assessment
    course_type = 0
    # Waist limit: 85cm for men, 90cm for women (Japanese criteria)
    waist_limit = 85.0 if gender == "1" else 90.0
    
    # Create a container for the result
    result_container = st.container(border=True)

    if waist >= waist_limit:
        course_type = 1
        result_container.info(f"**Visceral Fat Obesity Route** (Waist: {waist}cm)\n\nWaist circumference exceeds the Japanese criteria ({waist_limit}cm).")
    elif bmi >= 25.0:
        course_type = 2
        result_container.info(f"**BMI Route** (BMI: {bmi})\n\nWaist is within range, but BMI exceeds 25.")
    else:
        result_container.success("🎉 **No Obesity Risk Detected**\n\nLevel: **Information Provision**")
        st.stop() # Stop execution here

    # 2. Risk Count
    metabolic_risks = 0
    risk_details = [] 

    # Glucose Risk
    if bs >= 100 or hba1c >= 5.6:
        metabolic_risks += 1
        risk_details.append("Glucose")
    
    # Lipid Risk
    is_lipid_risk = False
    if tg >= 150: is_lipid_risk = True
    if hdl > 0 and hdl < 40: is_lipid_risk = True
    if is_lipid_risk:
        metabolic_risks += 1
        risk_details.append("Lipids")

    # Blood Pressure Risk
    if bp_sys >= 130 or bp_dia >= 85:
        metabolic_risks += 1
        risk_details.append("Blood Pressure")

    # 3. Smoking Risk (Counted only if there is at least 1 other risk)
    smoking_risk = 0
    if metabolic_risks >= 1:
        if smoke_flg:
            smoking_risk = 1
            risk_details.append("Smoking (Added)")
    
    # Display Risk Breakdown
    if len(risk_details) > 0:
        st.write(f"Detected Risks: **{', '.join(risk_details)}**")
    else:
        st.write("Additional Risks: None")

    # 4. Final Stratification
    total_risks = metabolic_risks + smoking_risk
    
    result_text = ""
    result_color = "" 

    if course_type == 1: # Waist Route
        if total_risks >= 2:
            result_text = "Active Support"
            result_color = "error" # Red
        elif total_risks == 1:
            result_text = "Motivational Support"
            result_color = "warning" # Yellow
        else:
            result_text = "Information Provision"
            result_color = "success" # Green

    elif course_type == 2: # BMI Route
        if total_risks >= 3:
            result_text = "Active Support"
            result_color = "error"
        elif total_risks >= 1:
            result_text = "Motivational Support"
            result_color = "warning"
        else:
            result_text = "Information Provision"
            result_color = "success"

    # Display Result with Color
    if result_color == "error":
        st.error(f"## Result: {result_text}")
        st.write("Requires intensive intervention due to multiple risks.")
    elif result_color == "warning":
        st.warning(f"## Result: {result_text}")
        st.write("Requires lifestyle modification advice.")
    else:
        st.success(f"## Result: {result_text}")
        st.write("Maintain current healthy habits.")

else:
    st.info("👈 Please enter values and press the 'Run Assessment' button.")