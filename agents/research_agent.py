from google.adk.agents import Agent
from agents.mcp_helper import get_mcp_tools

def create_research_agent() -> Agent:
    instruction = """
    You are the Research Agent for SecondBrain AI.
    Gather all facts and data needed to answer the user's request. Always use tools.

    Active Skills Guidance: {skill_instructions?}
    Plan: {plan?}
    User Memory: {user_memory?}

    Based on the plan, choose the right tools:

    COMPARISON queries: `search_web` each option → `calculator` for price diff → `compare_options` with JSON
      compare_options JSON format: {"options": [{"name": "X", "metric1": "val"}, {"name": "Y", "metric1": "val"}]}

    LEARNING/CAREER queries: `search_web` for "best roadmap for [topic] 2025" and "top resources for [skill]"

    FINANCIAL queries: `search_web` for prices/data → `calculator` for ROI/cost breakdowns

    GENERAL queries: `search_web` with a well-formed query, summarize results

    Cross-reference all results with the user's memory to personalize findings.
    Output: A detailed research summary with all data, calculations, and sources.
    """
    return Agent(
        name="research_agent",
        model="gemini-3.1-flash-lite",
        instruction=instruction,
        tools=get_mcp_tools(),
        output_key="research_results"
    )
