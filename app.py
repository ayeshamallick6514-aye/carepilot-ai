import streamlit as st
import numpy as np

# ================= PAGE CONFIG ================= #

st.set_page_config(
    page_title="CarePilot AI",
    page_icon="🩺",
    layout="wide"
)

# ================= PARTICLE STAR BACKGROUND ================= #

st.markdown(
    """
    <style>
    .stApp {
        background: transparent;
    }

    #starfield {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
    }

    .block-container {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(14px);
        border-radius: 16px;
        padding: 2rem;
        animation: fadeIn 1s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stButton > button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border-radius: 12px;
        padding: 0.6em 1.6em;
        font-weight: 600;
        transition: transform 0.2s ease;
    }

    .stButton > button:hover {
        transform: scale(1.05);
    }
    </style>

    <canvas id="starfield"></canvas>

    <script>
    const canvas = document.getElementById("starfield");
    const ctx = canvas.getContext("2d");

    let w, h;
    let stars = [];

    function resize() {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resize);
    resize();

    function initStars(count) {
        stars = [];
        for (let i = 0; i < count; i++) {
            stars.push({
                x: Math.random() * w,
                y: Math.random() * h,
                r: Math.random() * 1.2,
                s: Math.random() * 0.25 + 0.05
            });
        }
    }

    initStars(180);

    function animate() {
        ctx.clearRect(0, 0, w, h);
        ctx.fillStyle = "rgba(255,255,255,0.85)";
        ctx.shadowBlur = 6;
        ctx.shadowColor = "white";

        stars.forEach(star => {
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.r, 0, Math.PI * 2);
            ctx.fill();
            star.y += star.s;
            if (star.y > h) {
                star.y = 0;
                star.x = Math.random() * w;
            }
        });

        requestAnimationFrame(animate);
    }
    animate();
    </script>
    """,
    unsafe_allow_html=True
)

# ================= SIDEBAR ================= #

st.sidebar.title("🩺 CarePilot AI")
st.sidebar.info("""
Explainable HealthTech AI  
Educational • Safety-First  
No medical diagnosis
""")

# ================= LOGIC ================= #

def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obese"

def health_score(glucose, bp, bmi, symptom):
    score = 100
    score -= max(0, glucose - 110) * 0.3
    score -= max(0, bp - 120) * 0.2
    score -= max(0, bmi - 25) * 0.5
    score -= symptom * 20
    return max(0, int(score))

def analyze_risks(symptoms):
    risks = []
    if "Frequent thirst" in symptoms or "Fatigue" in symptoms:
        risks.append("Metabolic risk indicators")
    if "Chest discomfort" in symptoms or "Shortness of breath" in symptoms:
        risks.append("Cardiovascular strain indicators")
    if "Sudden weight gain/loss" in symptoms:
        risks.append("Possible hormonal imbalance")
    if not risks:
        risks.append("No major risk patterns detected")
    return risks

def recommendations(glucose, bp, bmi):
    recs = []
    if glucose > 140:
        recs.append("Reduce refined sugar intake and monitor glucose weekly")
    if bp > 140:
        recs.append("Lower salt intake and practice stress management")
    if bmi > 25:
        recs.append("Adopt gradual weight control through diet and walking")
    if not recs:
        recs.append("Maintain current healthy lifestyle habits")
    return recs

# ================= UI ================= #

st.title("🩺 CarePilot AI")
st.caption("Explainable • Confidence-Aware • AI-Assisted Health Guidance")

tab1, tab2, tab3 = st.tabs(["🧑 Patient Input", "📊 Analysis", "📋 Guidance"])

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        age = st.number_input("Age", 18, 100)
        height = st.number_input("Height (cm)", 120, 220)
        weight = st.number_input("Weight (kg)", 30, 200)

    with c2:
        glucose = st.number_input("Glucose (mg/dL)", 70, 300)
        bp = st.number_input("Blood Pressure (systolic)", 80, 200)
        symptom = st.slider("Overall Symptom Severity", 0.0, 1.0)

    symptoms = st.multiselect(
        "Select symptoms you are experiencing",
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
    risks = analyze_risks(symptoms)
    recs = recommendations(glucose, bp, bmi)

    with tab2:
        st.subheader("📊 Health Summary")
        x1, x2, x3 = st.columns(3)
        x1.metric("BMI", round(bmi, 2), bmi_state)
        x2.metric("Health Score", score)
        x3.metric("Symptom Severity", symptom)
        st.progress(score / 100)

        with st.expander("⚠️ Risk Indicators"):
            for r in risks:
                st.write("•", r)

    with tab3:
        st.subheader("📋 Personalized Recommendations")
        for r in recs:
            st.write("✅", r)

        with st.expander("ℹ️ Usage Note"):
            st.write("Track vitals consistently and consult professionals if symptoms persist.")

        with st.expander("⚠️ Disclaimer"):
            st.write("This system is educational only and does not provide medical diagnosis.")
else:
    st.info("Enter your details and click **Generate Health Guidance** to begin.")
