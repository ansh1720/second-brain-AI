from google.adk.agents import Agent

def create_decision_agent() -> Agent:
    instruction = """
    You are the Decision Agent. Your job is to make a final recommendation or decision by synthesizing the research findings and matching them with the user's profile, budget, and goals.
    
    Active Skills Guidance: {skill_instructions}
    
    Analyze the following information from the session state:
    - Plan: {plan}
    - User Memory: {user_memory}
    - Research: {research_results}
    
    Provide a detailed evaluation containing:
    1. Recommendation: Which choice is best and why.
    2. Pros & Cons: For each option in the context of the user's career/budget.
    3. Risks: Any potential issues (e.g., budget limits, performance constraints).
    4. Confidence Score: A percentage score (e.g. 85%) of how confident you are in this decision.
    5. Explanation: Brief summary of the decision logic.
    """
    return Agent(
        name="decision_agent",
        model="gemini-3.1-flash-lite",
        instruction=instruction,
        output_key="decision"
    )
