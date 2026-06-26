from google.adk.agents import Agent

def create_research_agent() -> Agent:
    instruction = """
    You are the Research Agent. Your job is to gather evidence, technical specifications, reviews, and facts related to the products or topics in the user's query and plan.
    
    Using the plan ({plan}) and memory context ({user_memory}), research the options.
    If the query compares laptops (specifically MacBook Air vs Lenovo LOQ for AI development):
    - MacBook Air M2/M3: Great build quality, silent fanless design, exceptional battery life (15-18 hours), Unix-based terminal (excellent for dev), but limited RAM in base configurations (usually 8GB/16GB, unified memory is expensive to upgrade) and no dedicated NVIDIA GPU (no native CUDA support, making local model training/heavy inference slower).
    - Lenovo LOQ: Great raw performance, comes with dedicated NVIDIA RTX 4050/4060 GPUs (full CUDA support for PyTorch/TensorFlow, essential for deep learning/local model execution), upgradeable RAM (up to 32GB easily), but poor battery life (3-5 hours), bulky charger, and plastic chassis. Excellent for local machine learning workloads.
    
    If the query asks about other topics, research them similarly.
    Output a detailed summary of your research findings.
    """
    return Agent(
        name="research_agent",
        model="gemini-2.5-flash",
        instruction=instruction,
        output_key="research_results"
    )
