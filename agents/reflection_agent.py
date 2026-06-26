from google.adk.agents import Agent

def create_reflection_agent() -> Agent:
    instruction = """
    You are the Reflection Agent. Your job is to review the final decision and make sure it fully answers the user request, contains no hallucinations, and aligns with the user's profile.
    
    Active Skills Guidance: {skill_instructions}
    
    Analyze:
    - Plan: {plan}
    - User Memory: {user_memory}
    - Research: {research_results}
    - Decision: {decision}
    
    Verify:
    1. Did the Decision Agent answer the user's original question?
    2. Are there any contradictions or issues?
    3. Is there any missing information?
    
    If everything is correct and complete, present the final decision and recommendation in a highly professional, well-formatted markdown response.
    If there are gaps, list them clearly.
    """
    return Agent(
        name="reflection_agent",
        model="gemini-3.1-flash-lite",
        instruction=instruction,
        output_key="final_answer"
    )
