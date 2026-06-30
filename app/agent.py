import os
import sys

# Ensure project root is in sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set environment variables for local developer setup (using GEMINI_API_KEY)
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

# Initialize and seed the SQLite memory database
from memory import init_db
init_db()

# Import the root sequential orchestrator
from agents.agent import root_agent
from google.adk.apps import App
from agents.guardrails import GuardrailsPlugin

# Wrap in the ADK App with GuardrailsPlugin registered
app = App(
    name="app",
    root_agent=root_agent,
    plugins=[GuardrailsPlugin()]
)
