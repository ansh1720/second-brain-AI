from google.adk.agents import Agent
from agents.mcp_helper import get_mcp_toolset

def create_research_agent() -> Agent:
    instruction = """
    You are the Research Agent. Your job is to gather evidence, technical specifications, reviews, and facts related to the products or topics in the user's query and plan.
    
    Using the plan ({plan}) and memory context ({user_memory}), research the options.
    
    You must:
    1. Call the `search_web` tool to search for details, benchmarks, and prices of MacBook Air M2/M3 vs Lenovo LOQ.
    2. Call the `calculator` tool to perform budget checks or calculations (e.g. calculate price differences).
    3. Call the `compare_options` tool with a JSON string comparing the laptops. Use this JSON format:
       {"options": [{"name": "MacBook Air M2", "price": "89,900 INR", "gpu": "Integrated Apple GPU (No CUDA)", "ram": "8GB Unified (soldered)", "battery": "18 hours"}, {"name": "Lenovo LOQ", "price": "70,000 INR", "gpu": "Dedicated NVIDIA RTX 4050 (CUDA)", "ram": "16GB (upgradeable)", "battery": "3-5 hours"}]}
    
    Output a detailed summary of your research findings, including the comparison table.
    """
    return Agent(
        name="research_agent",
        model="gemini-3.1-flash-lite",
        instruction=instruction,
        tools=[get_mcp_toolset()],
        output_key="research_results"
    )
