"""
The main orchestrator that builds and manages the LangGraph workflow.
"""

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

from shared.state import AgentState
from agents.agent_selector import AgentSelector
from agents.geo import GeographyAgent
from agents.culture import CultureAgent
from agents.lore import LoreAgent
from agents.ecnomics import EconomicsAgent
from agents.politics import PoliticsAgent


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
            "GeographyAgent": GeographyAgent(self.llm),
            "CultureAgent": CultureAgent(self.llm),
            "LoreAgent": LoreAgent(self.llm),
            "EconomicsAgent": EconomicsAgent(self.llm),
            "PoliticsAgent": PoliticsAgent(self.llm)
        }
        
        # Build the LangGraph workflow
        self.thread_memory = {} # Initialize empty thread memory
        self.current_thread_id = 1 # Default thread ID
        self.workflow = self._build_workflow()

   
    def _build_workflow(self) -> StateGraph:
        """
        Construct the LangGraph workflow that defines agent interactions.
        """
        # create state graph managing workflow
        workflow = StateGraph(AgentState)

        # entry point node
        workflow.add_node("agent_selector", self.selector.select_agent)  #select_agent is fnct name

        # Add nodes for each specialized agent
        workflow.add_node("GeographyAgent", self.agents["GeographyAgent"].process_request)
        workflow.add_node("CultureAgent", self.agents["CultureAgent"].process_request)
        workflow.add_node("LoreAgent", self.agents["LoreAgent"].process_request)
        workflow.add_node("EconomicsAgent", self.agents["EconomicsAgent"].process_request)
        workflow.add_node("PoliticsAgent", self.agents["PoliticsAgent"].process_request)
        
        # starting node
        workflow.set_entry_point("agent_selector")

        # add conditional routing from selector to agents
        workflow.add_conditional_edges(
            "agent_selector",
            self._route_to_agent,
            {
                "GeographyAgent": "GeographyAgent",
                "CultureAgent": "CultureAgent",
                "LoreAgent": "LoreAgent",
                "EconomicsAgent": "EconomicsAgent",
                "PoliticsAgent": "PoliticsAgent"
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

    # Thread
    def start_new_thread(self) -> int:
        """
        Start a fresh conversation thread. Clears all memory.
        Returns:
            New thread ID (always 1 for simplicity)
        """
        self.current_thread_id = 1
        # Clear all memory for fresh start
        if 1 in self.thread_memory:
            del self.thread_memory[1]
        
        print(f" Started fresh thread: {self.current_thread_id}")
        return self.current_thread_id

    
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
            "thread_id": thread_id,
            "thread_memory": self.thread_memory
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
        
        # Update thread memory - SLIDING WINDOW
        if final_response:
            # Create new memory entry
            memory_entry = MemoryEntry(
                prompt = user_input,
                responding_agent = result["selected_agent"],
                response = final_response,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

        # Initialize thread memory if this is a new thread
        if thread_id not in self.thread_memory:
            self.thread_memory[thread_id] = []
        
        # Add new entry to thread's memory
        self.thread_memory[thread_id].append(memory_entry)

        # SLIDING WINDOW: Keep only last 5 entries (remove oldest if > 5)
        if len(self.thread_memory[self.current_thread_id]) > 5:
            self.thread_memory[self.current_thread_id] = self.thread_memory[self.current_thread_id][-5:]
            
            # Show current memory status
        memory_count = len(self.thread_memory[self.current_thread_id])
        print(f" Memory: {memory_count}/5 interactions in sliding window")

        return {
            "response": final_response or "No response generated",
            "selected_agent": result["selected_agent"],
            "reasoning": result["agent_reasoning"],
            "full_conversation": result["messages"],
            "thread_id": self.current_thread_id,
            "memory_count": len(self.thread_memory.get(self.current_thread_id, []))
        }
        
