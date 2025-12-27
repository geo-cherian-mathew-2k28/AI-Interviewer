import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env file.")
else:
    print(f"✅ Found API Key: {api_key[:5]}...*****")
    
    try:
        genai.configure(api_key=api_key)
        print("🔍 Scanning for available models...")
        
        models = list(genai.list_models())
        found_any = False
        
        print("\n--- AVAILABLE MODELS ---")
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"🌟 {m.name}")
                found_any = True
        
        if not found_any:
            print("\n❌ No chat models found. Please check if 'Generative Language API' is enabled in Google Cloud Console.")
        else:
            print("\n✅ SUCCESS: Use one of the names above in your agents.py file.")
            
    except Exception as e:
        print(f"\n❌ CONNECTION ERROR: {e}")