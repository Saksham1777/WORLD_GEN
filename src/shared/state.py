"""
Shared state definitions and types used by all agents.
Acts as a "contract" that all components must follow.
"""

from typing import Dict, Any, List
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

class MemoryEntry(TypedDict):
    prompt: str
    responding_agent: str
    response: str
    timestamp: str

class AgentState(TypedDict):
    """
    The central state object that flows through our agent system.
    """
    messages : List[BaseMessage] # full conversation history
    selected_agent : str
    agent_reasoning : str
    input_prompt : str
    thread_id: int  # unique identifier for the conversation thread
    thread_memory: Dict[int, List[MemoryEntry]]

class AgentConfig(TypedDict):
    """
    Config structure of each agent.
    Defines agents capabilities and behaviour
    """
    description: str # what agent does
    system_prompt : str # agent core instructions
