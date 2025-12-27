<div align="center">
<br />
<img src="https://cdn-icons-png.flaticon.com/512/9131/9131529.png" alt="Nexus AI Logo" width="100">
<h1 align="center">NEXUS // ENTERPRISE</h1>

<p align="center">
<b>Autonomous Technical Recruiting Infrastructure</b>




<i>Privacy-First • Local Intelligence • Context-Aware</i>
</p>

<div align="center">
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Streamlit-FF4B4B%3Fstyle%3Dfor-the-badge%26logo%3Dstreamlit%26logoColor%3Dwhite" alt="Streamlit">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Ollama-Local_AI-000000%3Fstyle%3Dfor-the-badge%26logo%3Dapple%26logoColor%3Dwhite" alt="Ollama">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/LangChain-Integration-1C3C3C%3Fstyle%3Dfor-the-badge%26logo%3Dchainlink%26logoColor%3Dwhite" alt="LangChain">
</div>
</div>

⚡ Overview

Nexus AI is a next-generation autonomous interviewing agent designed to conduct technical screenings without human intervention. Powered by Ollama (Llama 3.2), it runs entirely on local hardware, ensuring zero data leakage and no API costs.

Unlike standard chatbots, Nexus features Context-Aware Logic: it dynamically recognizes when a coding challenge is required and reveals an inline, syntax-highlighted coding sandbox. Once the candidate submits their solution, the sandbox auto-hides to maintain a seamless conversational flow.

🚀 Key Features

<table>
<tr>
<td width="50%">
<h3>🧠 Neural Reasoning</h3>
<p>Uses local LLMs to parse PDF resumes and generate tailored technical questions based on the candidate's actual experience.</p>
</td>
<td width="50%">
<h3>💻 Smart Coding Sandbox</h3>
<p>Automatically detects technical intents (e.g., "Write a function...") and slides up a coding editor directly in the chat stream.</p>
</td>
</tr>
<tr>
<td>
<h3>✨ Enterprise UX</h3>
<p>Features a "Glassmorphism" design with deep dark modes, sticky headers, and animated transitions for a premium feel.</p>
</td>
<td>
<h3>🔒 Privacy First</h3>
<p>All processing happens on-device. No data is sent to the cloud, making it compliant with strict data privacy regulations.</p>
</td>
</tr>
</table>

🛠️ Installation Guide

Follow these steps to set up the project on your local machine.

1. Prerequisites

        Python 3.10 or higher installed.

Ollama installed and running. Download here.

2. Clone the Repository

        git clone [https://github.com/YourUsername/nexus_ai.git](https://github.com/YourUsername/nexus_ai.git)
        cd nexus_ai


3. Create Virtual Environment

It is recommended to use a virtual environment to keep dependencies clean.

Windows:

    python -m venv venv
    venv\Scripts\activate


Mac/Linux:

    python3 -m venv venv
    source venv/bin/activate


4. Install Dependencies

          pip install -r requirements.txt


5. Setup Local Brain

Open a separate terminal window and run Ollama. Then, pull the optimized model:

        ollama serve
      # In a new terminal:
        ollama pull llama3.2


🖥️ Usage

Start the Application:

    streamlit run app.py


Upload Profile:
Open the sidebar (arrow icon), upload a candidate's Resume (PDF), and click "Initialize Sequence".

The Interview:
Chat with Nexus. When the AI asks you to write code, the editor will appear automatically at the bottom.

Finish:
Click "Terminate Session" to end the interview and generate a final evaluation report.

📂 Project Structure

    nexus_ai/
    ├── app.py              # Main Application (UI & Logic)
    ├── agents.py           # AI Model Integration (Ollama + LangChain)
    ├── config.py           # System Prompts & Instructions
    ├── utils.py            # PDF Parsing Utilities
    ├── requirements.txt    # Python Dependencies
    └── README.md           # Documentation


<div align="center">
<p>Developed with ❤️ by <b>Geo Cherian Mathew</b></p>
</div>
