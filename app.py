import streamlit as st
import numpy as np

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="CarePilot AI",
    page_icon="🩺",
    layout="wide"
)

# ---------------- ANIMATED SPACE UI ---------------- #

st.markdown(
    """
    <style>
    /* Make Streamlit background transparent */
    .stApp {
        background: transparent;
    }

    /* Canvas full screen */
    #starfield {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
    }
    </style>

    <canvas id="starfield"></canvas>

    <script>
    const canvas = document.getElementById("starfield");
    const ctx = canvas.getContext("2d");

    let width, height;
    let stars = [];

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resize);
    resize();

    function createStars(count) {
        stars = [];
        for (let i = 0; i < count; i++) {
            stars.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 1.2,
                speed: Math.random() * 0.3 + 0.05
            });
        }
    }

    createStars(160);

    function drawStars() {
        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = "white";

        stars.forEach(star => {
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
            ctx.fill();

            star.y += star.speed;
            if (star.y > height) {
                star.y = 0;
                star.x = Math.random() * width;
            }
        });

        requestAnimationFrame(drawStars);
    }

    drawStars();
    </script>
    """,
    unsafe_allow_html=True
)


    @keyframes spaceMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glass effect containers */
    .block-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 2rem;
        animation: fadeIn 1.2s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border-radius: 12px;
        padding: 0.6em 1.5em;
        font-weight: bold;
        transition: transform 0.2s ease;
    }

    .stButton > button:hover {
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🩺 CarePilot AI")
st.sidebar.info("""
Explainable HealthTech AI  
Educational • Safety-First  
No medical diagnosis
""")

# ---------------- LOGIC ---------------- #

def calculate_bmi(weight, height):
    h = height / 100
    return weight / (h * h)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def health_score(glucose, bp, bmi, symptom):
    score = 100
    score -= max(0, glucose - 110) * 0.3
    score -= max(0, bp - 120) * 0.2
    score -= max(0, bmi - 25) * 0.5
    score -= symptom * 20
    return max(0, int(score))

def analyze_risk(symptoms):
    risks = []
    if "Frequent thirst" in symptoms or "Fatigue" in symptoms:
        risks.append("Possible metabolic imbalance")
    if "Chest discomfort" in symptoms or "Shortness of breath" in symptoms:
        risks.append("Possible cardiovascular strain")
    if "Sudden weight gain/loss" in symptoms:
        risks.append("Possible hormonal imbalance")
    if not risks:
        risks.append("No major risk indicators detected")
    return risks

def recommendations(glucose, bp, bmi):
    rec = []
    if glucose > 140:
        rec.append("Reduce sugar intake and monitor glucose weekly")
    if bp > 140:
        rec.append("Lower salt intake and manage stress")
    if bmi > 25:
        rec.append("Adopt gradual weight control via diet and walking")
    if not rec:
        rec.append("Maintain current healthy lifestyle")
    return rec

# ---------------- UI ---------------- #

st.title("🩺 CarePilot AI")
st.caption("Explainable • Confidence-Aware • AI-Assisted Health Guidance")

tab1, tab2, tab3 = st.tabs(["🧑 Patient Input", "📊 Analysis", "📋 Guidance"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 18, 100)
        height = st.number_input("Height (cm)", 120, 220)
        weight = st.number_input("Weight (kg)", 30, 200)

    with col2:
        glucose = st.number_input("Glucose (mg/dL)", 70, 300)
        bp = st.number_input("Blood Pressure (systolic)", 80, 200)
        symptom = st.slider("Overall Symptom Severity", 0.0, 1.0)

    symptoms = st.multiselect(
        "Select symptoms",
        [
            "Frequent thirst",
            "Fatigue",
            "Headache",
            "Chest discomfort",
            "Shortness of breath",
            "Sudden weight gain/loss",
            "Blurred vision"
        ]
    )

    run = st.button("🚀 Generate Health Guidance")

if run:
    bmi = calculate_bmi(weight, height)
    bmi_state = bmi_category(bmi)
    score = health_score(glucose, bp, bmi, symptom)
    risks = analyze_risk(symptoms)
    recs = recommendations(glucose, bp, bmi)

    with tab2:
        st.subheader("📊 Health Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("BMI", round(bmi, 2), bmi_state)
        c2.metric("Health Score", score)
        c3.metric("Symptom Severity", symptom)
        st.progress(score / 100)

        with st.expander("⚠️ Risk Indicators"):
            for r in risks:
                st.write("•", r)

    with tab3:
        st.subheader("📋 Recommendations")
        for r in recs:
            st.write("✅", r)

        with st.expander("ℹ️ Usage Note"):
            st.write("Follow suggestions gradually and consult professionals if symptoms persist.")

        with st.expander("⚠️ Disclaimer"):
            st.write("This system is educational only and not a medical diagnostic tool.")
else:
    st.info("Enter details and click **Generate Health Guidance** to begin.")
