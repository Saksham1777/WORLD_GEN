"""
The main orchestrator that builds and manages the LangGraph workflow.
"""

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

from shared.state import AgentState
from agents.agent_selector import AgentSelector
from agents.geo import GeographyAgent
from agents.culture import CultureAgent


class WorkFlowOrchestrator:
    """
    The conductor of our multi-agent orchestra. This class builds and manages
    the LangGraph workflow that coordinates all the agents.
    """

    def __init__(self, model_name: str = "gemini-2.0-flash-lite"):
        
        self.llm = ChatGoogleGenerativeAI(
            model = model_name,
            temperature = 0.0
        )
        # Setup agent selector and agents
        self.selector = AgentSelector(self.llm)
        self.agents = {
            "GeographyAgent" : GeographyAgent(self.llm),
            "CultureAgent"   : CultureAgent(self.llm),
        }
        # Build the LangGraph workflow
        self.workflow = self._build_workflow()

   
    def _build_workflow(self) -> StateGraph:
        """
        Construct the LangGraph workflow that defines agent interactions.
        """
        # create state graph managing workflow
        workflow = StateGraph(AgentState)

        # entry point node
        workflow.add_node("agent_selector", self.selector.select_agent)  #select_agent is fnct name

        # nodes for all agents
        # Add nodes for each specialized agent
        workflow.add_node("GeographyAgent", self.agents["GeographyAgent"].process_request)
        workflow.add_node("CultureAgent", self.agents["CultureAgent"].process_request)
    
        # starting node
        workflow.set_entry_point("agent_selector")

        # add conditional routing from selector to agents
        workflow.add_conditional_edges(
            "agent_selector",
            self._route_to_agent,
            {
                "GeographyAgent": "GeographyAgent",
                "CultureAgent": "CultureAgent",
            }
        )

        # After each agent is done, the workflow ends
        for agent_name in self.agents.keys():
            workflow.add_edge(agent_name, END)
          
        # Compile and return the workflow graph
        return workflow.compile()

    def _route_to_agent(self, state: AgentState ) -> str:
        """
        Routing function that determines the next agent based on selector decision.        
        Args:
            state: Current workflow state containing the selector's decision
        Returns:
            Name of the agent that should handle the request
        """
        return state["selected_agent"]

    def process_request(self, user_input : str) -> dict:
        """
        Process a user request through the complete multi-agent workflow.
        Args:
            user_input: The user's question or request
        Returns:
            Dictionary containing response and metadata about the process
        """
        
        initial_state = {
            "messages" : [],
            "selected_agent": "",
            "agent_reasoning": "",
            "input_prompt": user_input
        }

        # execute workflow
        result = self.workflow.invoke(initial_state)

        # extract final response
        final_response = None
        for message in reversed(result["messages"]):
            # Skip selector messages, get the actual agent response
            if hasattr(message, 'content') and not message.content.startswith("Selected"):
                final_response = message.content
                break
        
        return {
            "response": final_response or "No response generated",
            "selected_agent": result["selected_agent"],
            "reasoning": result["agent_reasoning"],
            "full_conversation": result["messages"]
        }
