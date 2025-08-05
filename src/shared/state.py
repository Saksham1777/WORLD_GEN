"""
Shared state definitions and types used by all agents.
Acts as "contract" that all componests must follow.
"""

from typing import Dict, Any, List
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

class AgentState(TypedDict):
    """
    The central state object that flows through our agent system.
    """
    messages : List[BaseMessage] # full convo history
    selected_agent : str
    agent_reasoning : str
    input_prompt : str # user input prompt 

class AgentConfig(TypedDict):
    """
    Config structure of each agent.
    Defines agents capabilites and behaviour
    """
    description: str # what agent does
    system_prompt : str # agent core instructions
