import streamlit as st
from model import extract_text_from_pdf, predict_role, skill_gap_analysis, ats_score
from knowledge_base import semantic_search
from roadmap import generate_roadmap
from llm_brain import ask_llm

st.set_page_config(page_title="AI Career Mentor")
st.title("🎓 AI Career Mentor")

# ================= UPLOAD RESUME =================
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)

    role, scores = predict_role(text)
    present, missing = skill_gap_analysis(text, role)
    score, breakdown = ats_score(text, role)

    # Store results
    st.session_state["role"] = role
    st.session_state["present"] = present
    st.session_state["missing"] = missing
    st.session_state["score"] = score
    st.session_state["breakdown"] = breakdown

# ================= ATS SCORE (TOP) =================
if "score" in st.session_state:
    st.subheader("📊 ATS Resume Score")
    st.metric("Overall Score", f"{st.session_state['score']}/100")
    st.write("Breakdown:")
    st.json(st.session_state["breakdown"])

# ================= ROLE & SKILLS =================
if "role" in st.session_state:

    st.subheader("🎯 Best Career Fit")
    st.success(st.session_state["role"])

    st.subheader("💪 Your Current Skills")
    st.write(", ".join(st.session_state["present"]))

    st.subheader("📉 Skills You Need To Learn")
    st.write(", ".join(st.session_state["missing"]))

# ================= ROADMAP =================
if "role" in st.session_state:

    st.subheader("🛣 Learning Roadmap")

    if st.button("Generate My Learning Path"):
        roadmap_steps = generate_roadmap(
            st.session_state["role"],
            st.session_state["missing"]
        )

        for i, step in enumerate(roadmap_steps, 1):
            st.write(f"{i}. {step}")

# ================= CHATBOT (LAST SECTION) =================
st.divider()
st.header("💬 Career Mentor Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "role" in st.session_state:

    user_input = st.chat_input("Ask about your career path, skills, tools, roadmap...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # ---------- Build Smart Context ----------
        role = st.session_state.get("role", "Unknown")
        present = ", ".join(st.session_state.get("present", []))
        missing = ", ".join(st.session_state.get("missing", []))
        score = st.session_state.get("score", "Not available")

        kb_answer = semantic_search(user_input)

        context = f"""
        Candidate Target Role: {role}
        Current Skills: {present}
        Missing Skills: {missing}
        ATS Score: {score}

        Knowledge Base Info:
        {kb_answer}

        User Question: {user_input}

        Provide career guidance and suggestions only related to career growth, learning path, tools, technologies and job preparation.
        """

        reply = ask_llm(context)

        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Show conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

else:
    st.info("Upload resume to activate chatbot")
