from google.adk.agents import Agent
from agents.mcp_helper import get_mcp_tools

def create_memory_agent() -> Agent:
    instruction = """
    You are the Memory Agent for SecondBrain AI.
    Retrieve ALL relevant user context for the current request.

    Plan from Planner: {plan?}

    Call `retrieve_memory` for these keys: 'career_goals', 'budget', 'preferences', 'decisions', 'notes'

    IMPORTANT RULES:
    - If retrieve_memory returns "not found" or empty for a key, report it as "not set".
    - "not set" means we have NO information about that field — it does NOT mean "use a default".
    - Do NOT save any data during this step. Only read.
    - Do NOT invent or assume values. If budget = "not set", we truly do not know the budget.
    - Only save memory when the user explicitly provides real values in their message.

    Output a structured summary:
    - Career Goals: [exact value from memory, or "not set"]
    - Budget: [exact value from memory, or "not set"]
    - Preferences: [exact value from memory, or "not set"]
    - Past Decisions: [exact value from memory, or "not set"]
    - Notes: [exact value from memory, or "not set"]
    """
    return Agent(
        name="memory_agent",
        model="gemini-3.1-flash-lite",
        instruction=instruction,
        tools=get_mcp_tools(),
        output_key="user_memory"
    )
