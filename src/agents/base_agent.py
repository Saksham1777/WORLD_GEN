"""
Base class for all specialized agents.
This provides common functionality and ensures consistent behavior.
"""

from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from shared.state import AgentState,AgentConfig

class BaseAgent(ABC):
    """
    Abstract base class that defines the interface all agents must implement.
    This ensures consistency and makes it easy to add new agent types.
    """

    def __init__(self, llm:ChatGoogleGenerativeAI ):
        self.llm = llm
        self.config = self.get_config()

    @abstractmethod
    def get_config(self) -> AgentConfig:
        """
        Each agent must define its own configuration.
        This method forces agents to explicitly declare their capabilities.
        """
        pass

    def process_request(self, state: AgentState) -> AgentState:
        """
        Standard method for processing requests that all agents share.
        This implements the common pattern while allowing customization.
        """
        # agent specialized prompt
        agent_prompt = ChatPromptTemplate.from_messages([
                ("system", self.config["system_prompt"]),
                ("human", "{input}")
            
        ])

        # process request with agent expretise
        formatted_prompt = agent_prompt.format_messages(
            input = state["input_prompt"]
        )

        response = self.llm.invoke(formatted_prompt)

        # return updated agent response to state
        return {
            **state,
            "messages" : state["messages"] + [response]
        }
