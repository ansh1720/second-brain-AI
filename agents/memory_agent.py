from google.adk.agents import Agent

def create_memory_agent() -> Agent:
    instruction = """
    You are the Memory Agent. Your job is to retrieve relevant information about the user's background, budget, preferences, and goals that could help customize the response.
    
    Examine the user request and the plan:
    - Plan: {plan}
    
    Simulate memory retrieval. If the user's query is about buying a laptop, career guidance, or dev environments, provide simulated preferences that match:
    - Career goals: Becoming an AI Engineer / AI Developer.
    - Budget: ₹70,000 INR (approx. $900 USD).
    - Preferred Brand: Open to any brand (Lenovo, Apple, etc.), but prefers value-for-money.
    
    Output a summary of these retrieved memories.
    """
    return Agent(
        name="memory_agent",
        model="gemini-2.5-flash",
        instruction=instruction,
        output_key="user_memory"
    )
