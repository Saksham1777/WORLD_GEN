# WORLD_GEN
# Multi-Agent Fantasy World Creator

A sophisticated multi-agent system that leverages LangGraph and Large Language Models to create immersive fantasy worlds through specialized AI agents. This project demonstrates advanced AI orchestration, memory management, and human-in-the-loop design patterns.

## Overview

This system employs five specialized AI agents that collaborate to generate comprehensive fantasy worlds based on user input. Each agent focuses on a specific domain expertise, ensuring rich, contextually aware world-building that maintains consistency across multiple interactions.

## Key Features

- **Multi-Agent Architecture**: Five specialized agents (Geography, Culture, Politics, Economics, Lore) working in orchestrated collaboration
- **Intelligent Agent Selection**: Automated routing system that selects the most appropriate agent based on user intent analysis
- **Memory Retention**: Sliding window memory system maintaining up to 5 previous conversations for contextual continuity
- **Human-in-the-Loop Design**: Interactive system allowing users to iteratively refine and modify generated content
- **Fallback Mechanism**: Robust error handling with automatic fallback to the Lore agent for generic requests
- **Thread Management**: Multi-threaded conversation support with isolated memory contexts - presently hardcoded. 

## Technical Architecture


### Core Components

**Orchestrator (`orchestrator.py`)**
- Central workflow manager built on LangGraph StateGraph
- Handles agent routing and state management
- Implements sliding window memory with configurable retention (current: 5 interactions)
- Manages conversation threads and context isolation

**Agent Selector (`agent_selector.py`)**
- Intelligent request analysis and agent routing
- JSON-based decision making with structured reasoning
- Keyword-based fallback selection for edge cases
- Real-time agent capability matching

**Base Agent (`base_agent.py`)**
- Abstract base class ensuring consistent agent behavior
- Standardized request processing pipeline
- Memory context integration for story continuity
- Template-based response generation

**Specialized Agents**
- **GeographyAgent**: Terrain, climate, and physical world features
- **CultureAgent**: Societies, customs, traditions, and settlements
- **PoliticsAgent**: Governance systems, power structures, authority
- **EconomicsAgent**: Trade systems, resources, economic structures
- **LoreAgent**: Narratives, histories, myths, and general storytelling

## Technology Stack

- **LangGraph**: Workflow orchestration and state management
- **LangChain**: Memory management and conversation handling  
- **Google Generative AI (Gemini)**: Large Language Model integration
- **Python**: Core implementation language
- **TypedDict**: Type-safe state management

## System Workflow

```
User Input → Agent Selector → Specialized Agent → Response Generation → Memory Update
↑ ↓
└── Human-in-the-Loop Feedback ←─────────────── Context Preservation ←──┘
```

## File Structure
```
WORLD_GEN/
├── src/
│   ├── agents/
│   │   ├── __pycache__/
│   │   ├── agent_selector.py
│   │   ├── base_agent.py
│   │   ├── culture.py
│   │   ├── economics.py
│   │   ├── geo.py
│   │   ├── lore.py
│   │   └── politics.py
│   ├── shared/
│   │   ├── __pycache__/
│   │   └── state.py
│   └── workflow/
│       ├── __pycache__/
│       ├── __init__.py
│       └── orchestrator.py
├── .env
└── main.py
```

## Installation
```
pip install langgraph langchain-google-genai langchain-core typing-extensions
```

## Usage Example
Set the .env file with your free gemini api key.

**Run the application**
```
python main.py
```
That's it! The interactive world creator will start, and you can begin building your fantasy world by typing your requests.


## Contributing
1. Extend the `BaseAgent` class for new agent types
2. Register new agents in the `WorkFlowOrchestrator` constructor
3. Update the `AgentSelector` with appropriate routing logic
4. Follow existing patterns for memory integration and state management

