from agents.base_agent import BaseAgent
from shared.state import AgentConfig


class CultureAgent(BaseAgent):
    def get_config(self) -> AgentConfig:
        return {
            "description": "Specializes in cultural studies; creates fictional cultures for a given geography.",
            "system_prompt": """
Write one vivid paragraph, ≈100 words, describing the CULTURE that thrives in this geography: {input}

Mandatory elements:
• Daily customs, values, or rituals.
• At least two named clans, tribes, or settlements.

Creative guidelines:
• Evocative, sensory language; inspire and entertain.
• Do NOT explain methodology or add commentary.

OUTPUT RULE: Return ONLY the culture paragraph—no headings, no lists, no analysis, no extra text.
"""
        }

