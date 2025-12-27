import streamlit as st
from pypdf import PdfReader
from gtts import gTTS
import speech_recognition as sr
import tempfile
import base64

def extract_text_from_pdf(pdf_file):
    if pdf_file is not None:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    return None

def text_to_speech(text):
    try:
        # Generate audio using Google TTS
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            return fp.name
    except:
        return None

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    # Hidden audio player that autoplays
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)

def recognize_speech():
    """Captures audio from microphone and returns text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("👂 Listening...", icon="🎙️")
        # Quick adjustment for background noise
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            # Listen for up to 5 seconds
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            st.toast("Processing...", icon="🔄")
            text = r.recognize_google(audio)
            return text
        except:
            return None