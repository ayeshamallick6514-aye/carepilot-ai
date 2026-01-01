import streamlit as st

st.set_page_config(
    page_title="CarePilot AI",
    page_icon="🩺",
    layout="wide"
)
st.title("🩺 CarePilot AI")
st.caption("Explainable, Confidence-Aware Health Guidance System")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧑 Patient Details")
    age = st.number_input("Age", 18, 100)
    glucose = st.number_input("Glucose (mg/dL)", 70, 300)
    bp = st.number_input("Blood Pressure", 80, 200)

with col2:
    st.subheader("📊 Health Indicators")
    bmi = st.number_input("BMI", 15.0, 45.0)
    symptom = st.slider("Symptom Severity", 0.0, 1.0)
    if st.button("Generate Guidance"):
        st.success("Guidance generated successfully ✅")
        if confidence == "High":
            st.success("Confidence Level: High")
        elif confidence == "Medium":
            st.warning("Confidence Level: Medium")
        else:
            st.error("Confidence Level: Low")



with st.expander("📚 Medical Context Used"):
    st.write(context)
    
    with st.expander("⚠️ Disclaimer"):
    st.write("This is educational guidance only.")
    st.sidebar.title("CarePilot AI")
    st.sidebar.info("""
An explainable HealthTech AI system.
Built with safety-first design.
""")





import numpy as np
import random
import faiss
from sentence_transformers import SentenceTransformer

# ---------------- Core Logic ---------------- #

def health_score(patient):
    score = 100
    score -= max(0, patient["glucose"] - 110) * 0.3
    score -= max(0, patient["bp"] - 120) * 0.2
    score -= max(0, patient["bmi"] - 25) * 0.5
    score -= patient["symptom_score"] * 20
    return max(score, 0)

def apply_advice(patient, advice):
    patient = patient.copy()
    if "glucose" in advice.lower():
        patient["glucose"] -= np.random.uniform(10, 25)
    if "pressure" in advice.lower():
        patient["bp"] -= np.random.uniform(8, 15)
    if "weight" in advice.lower():
        patient["bmi"] -= np.random.uniform(1, 3)
    patient["symptom_score"] *= np.random.uniform(0.6, 0.9)
    return patient

def estimate_confidence(before, after):
    improvement = after - before
    if improvement >= 15:
        return "High"
    elif improvement >= 5:
        return "Medium"
    else:
        return "Low"

def dynamic_policy(patient):
    advice = []
    if patient["glucose"] > 150:
        advice.append("glucose management")
    if patient["bp"] > 140:
        advice.append("blood pressure control")
    if patient["bmi"] > 25:
        advice.append("weight management")
    if not advice:
        advice.append("general wellness")
    return "Focus areas: " + ", ".join(advice)

# ---------------- RAG ---------------- #

docs = [
    "High glucose levels increase diabetes risk. Lifestyle changes help.",
    "High blood pressure affects heart health. Monitoring is advised.",
    "High BMI is linked to metabolic risks. Gradual weight control helps.",
    "Wellness habits improve long-term health."
]

model = SentenceTransformer("all-MiniLM-L6-v2")
doc_embeddings = model.encode(docs)
index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(doc_embeddings)

def retrieve_context(query):
    q_emb = model.encode([query])
    _, idx = index.search(q_emb, 1)
    return docs[idx[0][0]]

def explain(patient, advice, context, confidence):
    tone = random.choice(["calm", "supportive", "informative"])
    return f"""
**Tone:** {tone}

**Patient Summary**
- Age: {patient['age']}
- Glucose: {patient['glucose']:.1f}
- BP: {patient['bp']:.1f}
- BMI: {patient['bmi']:.1f}

**Advice**
{advice}

**Medical Context**
{context}

**Confidence Level**
{confidence}

⚠️ *This is educational guidance only, not a medical diagnosis.*
"""

# ---------------- UI ---------------- #

st.title("CarePilot AI 🩺")
st.subheader("Health Guidance System (Explainable & Confidence-aware)")

age = st.number_input("Age", 18, 100)
glucose = st.number_input("Glucose (mg/dL)", 70, 300)
bp = st.number_input("Blood Pressure (systolic)", 80, 200)
bmi = st.number_input("BMI", 15.0, 45.0)
symptom = st.slider("Symptom Severity", 0.0, 1.0)

if st.button("Generate Guidance"):
    patient = {
        "age": age,
        "glucose": glucose,
        "bp": bp,
        "bmi": bmi,
        "symptom_score": symptom
    }

    advice = dynamic_policy(patient)
    before = health_score(patient)
    after = health_score(apply_advice(patient, advice))
    confidence = estimate_confidence(before, after)
    context = retrieve_context(advice)

    st.markdown(explain(patient, advice, context, confidence))
