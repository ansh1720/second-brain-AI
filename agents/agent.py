from google.adk.agents import SequentialAgent
from agents.planner_agent import create_planner_agent
from agents.memory_agent import create_memory_agent
from agents.research_agent import create_research_agent
from agents.decision_agent import create_decision_agent
from agents.reflection_agent import create_reflection_agent

def create_orchestrator_agent() -> SequentialAgent:
    return SequentialAgent(
        name="orchestrator_agent",
        sub_agents=[
            create_planner_agent(),
            create_memory_agent(),
            create_research_agent(),
            create_decision_agent(),
            create_reflection_agent(),
        ],
    )

root_agent = create_orchestrator_agent()
