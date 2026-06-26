# Second Brain AI

An agentic system implementing a multi-agent "Second Brain" assistant. This project uses the Google Agent Development Kit (ADK), Model Context Protocol (MCP), and Gemini.

## Project Structure

```text
secondbrain-ai/
├── agents/        # Multi-agent architecture (Planner, Memory, Research, Decision, Reflection)
├── mcp/           # Model Context Protocol servers and connectors
├── skills/        # Custom tools and skills for agents
├── memory/        # Episodic and semantic memory systems
├── guardrails/    # Input/output safety and alignment validation
├── frontend/      # User interface
├── deployment/    # Infrastructure-as-code and configuration
├── docs/          # Project documentation
├── tests/         # Verification and evaluation tests
├── main.py        # Entrypoint / test script
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Setup Instructions

1. Ensure Python 3.11+ and Git are installed.
2. Initialize virtual environment:
   ```bash
   uv venv
   ```
3. Activate virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
5. Set up environment variables in `.env`:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
6. Run the test script:
   ```bash
   python main.py
   ```
