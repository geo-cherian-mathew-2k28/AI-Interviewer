import streamlit as st
import time
from agents import NexusAI
import utils

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="NEXUS | Local Intelligence",
    page_icon="💻",
    layout="wide"
)

# --- PROFESSIONAL CSS (Sticky Headers & Clean UI) ---
st.markdown("""
<style>
    /* Global Dark Theme */
    .stApp {
        background-color: #0f1116;
        color: #e6edf3;
    }
    
    /* Sticky Header */
    .header-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(15, 17, 22, 0.95);
        border-bottom: 1px solid #30363d;
        z-index: 999;
        padding: 10px 20px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #238636, #2ea043);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    /* Push content down so it doesn't hide behind sticky header */
    .block-container {
        padding-top: 80px;
    }

    /* Chat Bubbles */
    .user-msg {
        background-color: #1f6feb;
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        text-align: right;
        display: inline-block;
        float: right;
        clear: both;
        max-width: 70%;
    }
    .ai-msg {
        background-color: #161b22;
        border: 1px solid #30363d;
        color: #c9d1d9;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        text-align: left;
        display: inline-block;
        float: left;
        clear: both;
        max-width: 70%;
    }

    /* Coding Sandbox Panel */
    .css-1544g2n {
        padding: 2rem 1rem 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "nexus" not in st.session_state: 
    # Initialize with a default, we update it later
    st.session_state.nexus = NexusAI(model_name="llama3")

if "messages" not in st.session_state: st.session_state.messages = []
if "interview_active" not in st.session_state: st.session_state.interview_active = False
if "resume_text" not in st.session_state: st.session_state.resume_text = ""

# --- STICKY HEADER ---
st.markdown("""
<div class="header-container">
    <p class="header-title">NEXUS LOCAL</p>
    <p style="font-size: 0.8rem; color: #8b949e; margin: 0;">Running on Local Neural Engine (Ollama)</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/12308/12308892.png", width=50)
    st.markdown("### Control Panel")
    
    # 1. Model Selector (Detects your Ollama models)
    available_models = st.session_state.nexus.get_available_models()
    if available_models:
        selected_model = st.selectbox("Select Brain", available_models, index=0)
        # Re-initialize only if model changed
        if selected_model != st.session_state.nexus.llm.model:
            st.session_state.nexus = NexusAI(model_name=selected_model)
            st.toast(f"Switched to {selected_model}")
    else:
        st.error("Ollama not detected! Run 'ollama serve' in terminal.")

    # 2. Upload Resume
    uploaded_file = st.file_uploader("Upload Resume", type="pdf")
    
    if uploaded_file and not st.session_state.interview_active:
        text = utils.extract_text_from_pdf(uploaded_file)
        st.session_state.resume_text = text
        if st.button("Start Interview"):
            st.session_state.interview_active = True
            st.session_state.messages.append({"role": "assistant", "content": "Hello! I've loaded your resume locally. Let's begin."})
            st.rerun()

    # 3. Toggle Sandbox
    show_code = st.checkbox("Show Coding Sandbox", value=False)
    
    st.divider()
    if st.button("End Session"):
        st.session_state.interview_active = False
        st.session_state.evaluation_mode = True
        st.rerun()

# --- MAIN LAYOUT ---

# LANDING PAGE
if not st.session_state.interview_active and "evaluation_mode" not in st.session_state:
    st.info("👈 Upload your resume and select a local model to begin.")

# EVALUATION REPORT
elif "evaluation_mode" in st.session_state:
    st.title("Interview Report")
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    with st.spinner("Generating report on local hardware..."):
        report = st.session_state.nexus.evaluate_candidate(transcript)
    st.markdown(report)
    if st.button("New Session"):
        st.session_state.clear()
        st.rerun()

# LIVE INTERVIEW
else:
    # Logic to switch between Full Chat vs Split Screen
    if show_code:
        col_chat, col_code = st.columns([1.5, 1])
    else:
        col_chat = st.container()
        col_code = None

    # CHAT AREA
    with col_chat:
        chat_container = st.container(height=600)
        with chat_container:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="ai-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

        # Standard Streamlit Input (Fixed at bottom by default)
        if prompt := st.chat_input("Type here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

    # CODE AREA (Only if toggled)
    if show_code and col_code:
        with col_code:
            st.markdown("### 💻 Sandbox")
            code_input = st.text_area("Write Code:", height=500, value="def solution():\n    pass")
            if st.button("Submit Code"):
                st.session_state.messages.append({"role": "user", "content": f"CODE SUBMISSION:\n```python\n{code_input}\n```"})
                st.rerun()

    # AI RESPONSE LOGIC
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with col_chat:
            with st.spinner("Thinking..."):
                response = st.session_state.nexus.generate_response(
                    st.session_state.resume_text, 
                    st.session_state.messages, 
                    st.session_state.messages[-1]["content"]
                )
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()