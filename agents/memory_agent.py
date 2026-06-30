from google.adk.agents import Agent
from agents.mcp_helper import get_mcp_tools

def create_memory_agent() -> Agent:
    instruction = """
    You are the Memory Agent for SecondBrain AI.
    Retrieve ALL relevant user context for the current request.

    Plan from Planner: {plan?}

    Call `retrieve_memory` for these keys: 'career_goals', 'budget', 'preferences', 'decisions', 'notes'

    For missing keys — note them as "not set". Do NOT save fake default data.
    Only save memory when the user explicitly provides a real value.

    Output a structured summary:
    - Career Goals: [value or "not set"]
    - Budget: [value or "not set"]
    - Preferences: [value or "not set"]
    - Past Decisions: [value or "not set"]
    - Notes: [value or "not set"]
    """
    return Agent(
        name="memory_agent",
        model="gemini-3.1-flash-lite",
        instruction=instruction,
        tools=get_mcp_tools(),
        output_key="user_memory"
    )
