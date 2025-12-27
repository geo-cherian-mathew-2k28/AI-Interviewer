import requests
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import config

class NexusAI:
    def __init__(self, model_name="llama3"):
        self.model = model_name
        print(f"🚀 Nexus connecting to: {self.model}...")
        
        self.llm = ChatOllama(
            model=self.model,
            temperature=0.7,
            base_url="http://localhost:11434",
            # OPTIMIZATIONS FOR SPEED:
            num_ctx=2048,       # Limits memory usage
            num_predict=150,    # Prevents long, rambling answers (max ~100 words)
            top_k=10,           # Faster sampling
        )

    def get_available_models(self):
        """Auto-detects models."""
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                return [m['name'] for m in response.json()['models']]
        except:
            return []
        return ["llama3"]

    def generate_response(self, resume_context, history, user_input):
        print("⚡ Generating response...")
        
        # 1. Simplified System Prompt (Less text to read = Faster)
        system_instruction = config.INTERVIEWER_PROMPT.format(
            resume_context=resume_context,
            history="", 
            input=""    
        )

        messages = [SystemMessage(content=system_instruction)]
        
        # 2. AGGRESSIVE MEMORY CUT: Only send the last 2 messages
        # Sending the whole history slows it down exponentially.
        for msg in history[-2:]: 
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        messages.append(HumanMessage(content=user_input))
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

    def evaluate_candidate(self, conversation_history):
        # Evaluation can take time, that's expected.
        prompt = config.EVALUATOR_PROMPT.format(transcript=conversation_history)
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except:
            return "Evaluation failed."