import requests
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import config

class NexusAI:
    def __init__(self, model_name="llama3.2"):
        self.model = model_name
        print(f"🔌 Nexus connecting to: {self.model}...")
        
        self.llm = ChatOllama(
            model=self.model,
            temperature=0.7,
            base_url="http://localhost:11434",
            num_ctx=4096,       # Increased Context Window (Remember more conversation)
            num_predict=-1,     # CHANGED: -1 means 'Generate until finished' (No cutoff)
        )

    def generate_response(self, resume_context, history, user_input):
        print("⚡ Generating response...")
        
        system_instruction = config.INTERVIEWER_PROMPT.format(
            resume_context=resume_context,
            history="", 
            input=""    
        )

        messages = [SystemMessage(content=system_instruction)]
        
        # Keep last 6 messages for context
        for msg in history[-6:]: 
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        messages.append(HumanMessage(content=user_input))
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"System Error: Is Ollama running? ({str(e)})"

    def evaluate_candidate(self, conversation_history):
        prompt = config.EVALUATOR_PROMPT.format(transcript=conversation_history)
        try:
            # Evaluation needs to be long, so we ensure no cutoff here too
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except:
            return "Evaluation failed."