import streamlit as st
import time
from agents import NexusAI
import utils

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NEXUS | Enterprise AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PROFESSIONAL DESIGN SYSTEM (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #050505 60%);
        font-family: 'Inter', sans-serif;
    }

    /* HIDE STREAMLIT BRANDING */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    
    /* CHAT BUBBLES */
    .stChatMessage[data-testid="stChatMessage"] { background-color: transparent; }
    
    div[data-testid="stChatMessage"]:has(div[aria-label="assistant"]) div[data-testid="stChatMessageContent"] {
        background: #0f0f11;
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: #e0e0e0;
        border-left: 3px solid #818cf8;
        border-radius: 12px;
        width: 100%; 
    }

    div[data-testid="stChatMessage"]:has(div[aria-label="user"]) div[data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #2563eb, #1e40af);
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
    }
    
    div[data-testid="stChatMessage"] .st-emotion-cache-1p1m4tp { background-color: #2563eb; }

    /* HEADER */
    .glass-header {
        position: fixed; top: 0; left: 0; width: 100%; height: 60px;
        background: rgba(5, 5, 5, 0.8); backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        z-index: 999; display: flex; align-items: center; padding-left: 80px; 
    }
    .header-text { font-weight: 700; color: #fff; font-size: 1.1rem; letter-spacing: 1px; }
    .status-badge { margin-left: 20px; font-size: 0.75rem; background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 8px; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.2); }

    /* --- THE FIX: FIXED POSITIONING SIDEBAR --- */
    .sandbox-container {
        position: fixed;
        top: 80px;         /* 80px from top */
        right: 20px;       /* 20px from right edge */
        width: 45%;        /* Takes up 45% of screen */
        height: auto;
        z-index: 9999;      /* Stays ON TOP of everything */
        
        border: 1px solid #333;
        border-radius: 12px;
        background-color: rgba(10, 10, 15, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: -10px 10px 30px rgba(0,0,0,0.5);
        padding: 10px;
        animation: slideInRight 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
    }

    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(100px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Code Editor Styling */
    .stTextArea textarea {
        background-color: #0d0d0d !important;
        color: #00ff41 !important;
        font-family: 'Consolas', monospace;
        border: none !important;
    }
    
    /* Limit Chat Width when Sandbox is Open */
    .chat-narrow {
        max-width: 50% !important;
    }

    .block-container { padding-top: 5rem; }
</style>
""", unsafe_allow_html=True)

# --- STATE ---
if "nexus" not in st.session_state: st.session_state.nexus = NexusAI(model_name="llama3.2")
if "messages" not in st.session_state: st.session_state.messages = []
if "interview_active" not in st.session_state: st.session_state.interview_active = False
if "resume_text" not in st.session_state: st.session_state.resume_text = ""
if "show_sandbox" not in st.session_state: st.session_state.show_sandbox = False

# --- TRIGGER LOGIC ---
def detect_coding_intent(messages):
    if not messages: return False
    for msg in reversed(messages):
        if msg["role"] == "assistant":
            content = msg["content"].lower()
            trigger_words = [
                "write a function", "write code", "write a program", "create a class", 
                "define a class", "implement", "code this", "coding challenge", "solution", 
                "algorithm", "linked list", "array", "recursion", "object oriented",
                "sql query", "database", "html", "css", "react", "component", "python", "java"
            ]
            if any(word in content for word in trigger_words): return True
            if "thank you" in content or "next question" in content:
                if not any(word in content for word in trigger_words): return False
            return False 
    return False

# --- HEADER ---
st.markdown("""
<div class="glass-header">
    <span class="header-text">NEXUS // INTELLIGENCE</span>
    <span class="status-badge">● ONLINE</span>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9131/9131529.png", width=40)
    st.markdown("### Control Hub")
    
    uploaded_file = st.file_uploader("Upload Profile (PDF)", type="pdf")
    
    if uploaded_file and not st.session_state.interview_active:
        with st.spinner("Processing..."):
            text = utils.extract_text_from_pdf(uploaded_file)
            st.session_state.resume_text = text
            time.sleep(0.5)
            
        if st.button("Initialize Sequence", type="primary", use_container_width=True):
            st.session_state.interview_active = True
            st.session_state.messages.append({"role": "assistant", "content": "Identity verified. I am Nexus. Let's examine your technical background. Please introduce yourself."})
            st.rerun()

    st.divider()
    if st.button("Terminate Session", use_container_width=True):
        st.session_state.interview_active = False
        st.session_state.evaluation_mode = True
        st.rerun()

# --- MAIN LOGIC ---

# 1. LANDING PAGE
if not st.session_state.interview_active and "evaluation_mode" not in st.session_state:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_m = st.columns([1,2,1])[1]
    with col_m:
        st.markdown("<h1 style='text-align: center; font-size: 3.5rem; color: white;'>NEXUS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Autonomous Recruiting Infrastructure</p>", unsafe_allow_html=True)
        st.info("👈 Upload Resume in Sidebar to Begin")

# 2. EVALUATION
elif "evaluation_mode" in st.session_state:
    st.title("Final Assessment")
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    with st.spinner("Compiling Final Report..."):
        report = st.session_state.nexus.evaluate_candidate(transcript)
    st.markdown(report)
    if st.button("Re-Initialize"):
        st.session_state.clear()
        st.rerun()

# 3. LIVE INTERFACE
else:
    # --- AUTO-DETECT STATE ---
    st.session_state.show_sandbox = detect_coding_intent(st.session_state.messages)

    # --- CHAT CONTAINER (Responsive Width) ---
    # If sandbox is open, we only use half the screen for chat
    if st.session_state.show_sandbox:
        col_chat = st.columns([1, 1])[0] 
    else:
        col_chat = st.container()

    with col_chat:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar="⚡"):
                    st.markdown(msg["content"])

    # --- FIXED FLOATING SANDBOX ---
    if st.session_state.show_sandbox:
        # We put this in a generic container, but CSS handles the positioning
        st.markdown('<div class="sandbox-container">', unsafe_allow_html=True)
        
        c1, c2 = st.columns([8, 2])
        c1.info("⚡ Technical Challenge Active")
        
        code_input = st.text_area(
            "Code Editor", 
            value="def solution():\n    # Write efficient code here\n    pass", 
            height=400,
            label_visibility="collapsed"
        )
        
        if st.button("⚡ Execute & Submit", type="primary", use_container_width=True):
            formatted_code = f"**CODE SUBMISSION:**\n```python\n{code_input}\n```"
            st.session_state.messages.append({"role": "user", "content": formatted_code})
            st.toast("Code uploaded to Neural Engine", icon="🚀")
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

    # --- INPUT FIELD ---
    if prompt := st.chat_input("Input response..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # --- AI PROCESSING ---
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with col_chat:
            with st.chat_message("assistant", avatar="⚡"):
                with st.spinner("Thinking..."):
                    response = st.session_state.nexus.generate_response(
                        st.session_state.resume_text, 
                        st.session_state.messages, 
                        st.session_state.messages[-1]["content"]
                    )
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()