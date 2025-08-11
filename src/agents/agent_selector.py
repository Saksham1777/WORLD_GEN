import json
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from shared.state import AgentState
from agents.geo import GeographyAgent
from agents.culture import CultureAgent


class AgentSelector:
    """Select the best specialised agent for the user request."""
    
    def __init__(self, llm:ChatGoogleGenerativeAI):
        self.llm = llm
        self.available_agents = {
            "GeographyAgent" : GeographyAgent(self.llm),
            "CultureAgent"   : CultureAgent(self.llm),
            "LoreAgent" : LoreAgent(self.llm),
            "EconomicsAgent": EconomicsAgent(self.llm),
            "PoliticsAgent": PoliticsAgent(self.llm)
        }

    def select_agent(self, state:AgentState) -> AgentState:
        """
        Analyze the user's request and determine the most appropriate agent.
        """    
        # Input Validation
        if "input_prompt" not in state:
            print("ERROR: input_prompt not found in state!")
            return state

        # Agent Description Gathering
        try:
            agent_descriptions = {}
            for name, agent in self.available_agents.items():
                agent_descriptions[name] = agent.config["description"]
                print(f"Agents Available \n{name}: {agent_descriptions[name]}")
        except Exception as e:
            print(f"ERROR - Could not get agent descriptions: {e}")
            return self._create_fallback_state(state, f"Agent config error: {e}")


        # Prompt Construction
        selector_prompt = ChatPromptTemplate.from_messages([
            ("system", """
             You are an intelligent agent selector with a deep understanding of different types of requests and agent capabilities.
             Available agents and their specializations:
                1. GeographyAgent: {geo_agent_desc}
                2. CultureAgent: {culture_agent_desc}
                3. LoreAgent: {lore_agent_desc}
                4. PoliticsAgent: {politics_agent_desc}
                5. EconomicsAgent: {economics_agent_desc}
             CRITICAL: Respond with ONLY valid JSON in this EXACT format:
                {{"selected_agent": "GeographyAgent", "reasoning": "your reason here"}}
                OR
                {{"selected_agent": "CultureAgent", "reasoning": "your reason here"}}
             Rules:
                - selected_agent must be exactly "GeographyAgent" or "CultureAgent"
                - No text before or after the JSON
                - Use double quotes for all strings
                - No trailing commas
             
             Consider edge cases where a request might fit multiple categories - choose the agent whose core strengths best match the primary need."""),
            ("human", "Please analyze this request and select the best agent: {input}")
        ])

        # formatting prompt
        formated_prompt = selector_prompt.format_messages(
                geo_agent_desc = agent_descriptions["GeographyAgent"],
                culture_agent_desc = agent_descriptions["CultureAgent"],
                lore_agent_desc = agent_descriptions["LoreAgent"],
                politics_agent_desc = agent_descriptions["PoliticsAgent"],
                economics_agent_desc = agent_descriptions["EconomicsAgent"],
                input = state["input_prompt"]
        )

        # get selector's decision
        try:
            print("-----------------LLM Calling---------------")
            response = self.llm.invoke(formated_prompt)        
        except Exception as e:
            print(f"DEBUG - LLM call failed: {type(e).__name__}")
            print(f"DEBUG - Error details: {str(e)}")
            print(f"DEBUG - Formatted prompt: {formated_prompt}")
            raise e

        try:
            # Response Parsing
            decision = json.loads(response.content)
            selected_agent = decision["selected_agent"]
            reasoning = decision["reasoning"]

            # Agent Validation
            if selected_agent not in self.available_agents:
                raise ValueError(f"Unknown agent: {selected_agent}")
            
            # State Update
            state_update: AgentState = {
                **state,
                "selected_agent": selected_agent,
                "agent_reasoning": reasoning,
                "messages": state["messages"] + [AIMessage(content=f"Selected {selected_agent}: {reasoning}")]
            }
            return state_update
        

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            selected_agent = self._fallback_selection(state["input_prompt"])
            reasoning = f"Fallback selection due to parsing error: {str(e)}"

            state_update: AgentState  = {
                **state,
                "selected_agent": selected_agent,
                "agent_reasoning": reasoning,
                "messages": state["messages"] + [AIMessage(content= f"Selected {selected_agent} : {reasoning}")] #give values not key
            }
            return state_update
        
    def _fallback_selection(self, input_text: str) -> str:
        text_lower = input_text.lower()

        # Geography keywords
        geography_keywords = ["geography", "terrain", "world", "rocky", "mountain", "desert", "forest"]
        
        # Culture keywords  
        culture_keywords = ["culture", "people", "society", "community", "tradition"]

        # Lore keywords
        lore_keywords = ["story", "lore","plot", "tale", "history"]

        # Economics keywords
        ecnomics_keywords = ["economics", "trade", "market", "resources", "wealth"]

        # Politics keywords
        politics_keywords = ["politics", "government", "power", "leadership", "authority"]

        # Count keyword matches
        geography_score = sum(1 for keyword in geography_keywords if keyword in text_lower)
        culture_score = sum(1 for keyword in culture_keywords if keyword in text_lower)
        lore_score = sum(1 for keyword in lore_keywords if keyword in text_lower)
        ecnomics_score = sum(1 for keyword in ecnomics_keywords if keyword in text_lower)
        politics_score = sum(1 for keyword in politics_keywords if keyword in text_lower)

        # Store scores in a dictionary
        scores = {
                "GeographyAgent": geography_score,
                "CultureAgent": culture_score,
                "LoreAgent": lore_score,
                "EcnomicsAgent": ecnomics_score,
                "PoliticsAgent": politics_score
        }

        score_values = list(scores.values())

        # Edge case: all scores are the same (including all zeros)
        if score_values.count(score_values[0]) == len(score_values):
            return "LoreAgent"

        # Otherwise, select agent with highest score
        agent_selected = max(scores, key=scores.get)
        return agent_selected
