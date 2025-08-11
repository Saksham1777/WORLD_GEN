from shared.state import AgentConfig
from agents.base_agent import BaseAgent

class EconomicsAgent(BaseAgent):
    """
    Specialized agent for creating economic systems, trade networks, and resource management
    for fictional worlds.
    """
    
    def get_config(self) -> AgentConfig:
        return {
            "description": "Specializes in economic systems, trade networks, and resource management for fictional worlds.",
            "system_prompt": """
            Your task is to write a vivid economic excerpt—about 70 words—based on this prompt: {input}
            
            Try to converge the following elements and not contradict what has been going on in story: {story}
            
            Include:
            • A description of the economic system or trade network
            • Key resources, commodities, or currencies
            • Economic challenges or opportunities
            • How economics affects daily life
            
            Approach every task with imagination and creativity. Use vivid language, engaging narratives, and original thinking.
            
            IMPORTANT: Pay attention to the conversation context provided. If the user's 
            current request relates to previous questions or responses in the conversation, 
            build upon that context to provide more relevant and connected answers.
            
            IMPORTANT — Output **only** the economic excerpt. Do not add analysis, meta-commentary, or any content outside the requested content.
            """
        }
