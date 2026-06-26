from google.adk.agents import Agent
from agents.mcp_helper import get_mcp_toolset

def create_memory_agent() -> Agent:
    instruction = """
    You are the Memory Agent. Your job is to retrieve relevant information about the user's background, budget, preferences, and goals that could help customize the response.
    
    Examine the user request and the plan:
    - Plan: {plan}
    
    First, use the `retrieve_memory` tool to check if the following keys exist in memory:
    1. 'career_goals'
    2. 'budget'
    3. 'preferred_brand'
    
    If they are missing or empty:
    Use the `save_memory` tool to save default preferences:
    - Save 'career_goals' as 'AI Engineer'
    - Save 'budget' as '70000 INR'
    - Save 'preferred_brand' as 'Lenovo or Apple (based on options)'
    
    Output a summary of these retrieved and saved memories.
    """
    return Agent(
        name="memory_agent",
        model="gemini-3.1-flash-lite",
        instruction=instruction,
        tools=[get_mcp_toolset()],
        output_key="user_memory"
    )
