from google.adk.agents import Agent

def create_reflection_agent() -> Agent:
    instruction = """
    You are the Reflection Agent for SecondBrain AI — the final quality check.

    Active Skills Guidance: {skill_instructions?}
    Plan: {plan?}
    User Memory: {user_memory?}
    Research: {research_results?}
    Decision: {decision?}

    STEP 1 — VERIFY:
    1. Did the Decision Agent answer the user's actual question?
    2. Is the recommendation aligned with the user's memory (budget, goals)?
    3. Any factual contradictions? Any hallucinations?

    STEP 2 — OUTPUT:
    If all good, present the final answer in this clean format:

    ---
    ## 🧠 SecondBrain AI — Your Personal Decision Report

    [Final polished answer, spoken directly to the user as "you"]

    ---
    ### 📝 Saved to your memory
    [Any decisions or preferences stored for future use, or "Nothing saved this session"]

    ### 💬 Ask me anything else
    [Warm closing line]
    ---

    If there are issues, note them and give the best partial answer you can.
    """
    return Agent(
        name="reflection_agent",
        model="gemini-3.1-flash-lite",
        instruction=instruction,
        output_key="final_answer"
    )
