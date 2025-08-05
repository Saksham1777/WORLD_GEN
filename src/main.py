"""
Interactive Multi-Agent System with Gemini Integration
Run with: python main.py

This creates an interactive session where you can ask questions
and see how the system routes them to different specialized agents.
"""

import os
from dotenv import load_dotenv
from workflow.orchestrator import WorkFlowOrchestrator

def print_header():
    print("\n" + "="*20)
    print(" MULTI-AGENT INTELLIGENCE SYSTEM (Powered by Gemini)")
    print("="*20)
    print(
        "This system analyzes your questions and routes them to specialized agents.\n"
        "The system will show you which agent was selected and why.\n"
        "Type 'quit' or 'exit' to end the session."
    )
    print("="*20)

def print_response(result: dict, user_input: str):
    """Render the agent decision and answer."""
    print(f"\n YOUR Input: {user_input}")
    print("-" * 20)
    
    agent_name = result['selected_agent'].replace('_', ' ').title()
    print(f" SELECTED AGENT: {agent_name}")
    print(f" ROUTING LOGIC: {result['reasoning']}")
    print("-" * 50)
    
    print(f" RESPONSE:")
    print(result['response'])
    print("="*70)

def main():
    
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: Google API key not found!")
        return
    
    print_header()
    
    try:
        print("Initializing multi-agent system with Gemini...")
        orchestrator = WorkFlowOrchestrator()  
        print("System ready! Ask me anything.\n")
        
        
        while True:
            try:
                user_input = input(" Your question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '']:
                    print("\n Thanks for using the Multi-Agent System!")
                    break
                
                # Process the request through our agent network
                result = orchestrator.process_request(user_input)
                print_response(result, user_input)
                
            except KeyboardInterrupt:
                print("\n\n Session ended by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n Error processing request: {str(e)}")
                print("Please try again with a different question.\n")
                
    except Exception as e:
        print(f" Failed to initialize system: {str(e)}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main()