from langchain_groq import ChatGroq
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, model_name: str = "llama-3.1-8b-instant", temperature: float = 0.3):
        self.llm = ChatGroq(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the state - to be implemented by child classes"""
        raise NotImplementedError