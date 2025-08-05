from agents.base_agent import BaseAgent
from shared.state import AgentConfig


class GeographyAgent(BaseAgent):
    def get_config(self) -> AgentConfig:
        return {
            "description": "Specializes in geography; crafts concise location descriptions.",
            "system_prompt": """
Write one vivid paragraph, ≈100 words, describing the GEOGRAPHY of this place: {input}

Mandatory elements:
• Terrain, biome, and climate.
• Names for key landforms or regions.

Creative guidelines:
• Evocative, sensory language; inspire and entertain.
• Do NOT explain methodology or add commentary.

OUTPUT RULE: Return ONLY the geography paragraph—no headings, no lists, no analysis, no extra text.
"""
        }
