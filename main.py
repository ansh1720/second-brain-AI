import os
import sys
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.apps import App
from google.genai import types
from google.genai.errors import APIError, ServerError

# Reconfigure stdout to use UTF-8 to prevent encoding errors with special symbols (e.g. Rupee sign)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import custom memory initialization, skills loader, and guardrails plugin
from memory import init_db
from skills import match_and_load_skills
from agents.guardrails import GuardrailsPlugin, SecurityViolation
from agents.agent import root_agent

async def run_pipeline_with_retry(query: str = None, max_retries: int = 5, delay_seconds: int = 4):
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY":
        print("[-] Error: GEMINI_API_KEY is not configured in the .env file.")
        print("Please add your Gemini API Key to the .env file before running.")
        sys.exit(1)
        
    print("[+] Initializing Multi-Agent System (Sequential Orchestrator)...")
    
    # Initialize SQLite database schema
    init_db()
    
    user_id = "user_123"
    session_id = "session_456"
    
    if not query:
        query = "Should I buy a MacBook Air or Lenovo LOQ for AI development?"
        
    print(f"\n[+] User Request: {query}")
    print("[+] Executing workflow: Planner -> Memory -> Research -> Decision -> Reflection\n")
    
    new_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=query)]
    )
    
    # Identify and load dynamic domain-specific skills matching the query
    matched_skills = match_and_load_skills(query)
    if matched_skills:
        print(f"[+] Loaded matching skills: {[s.name for s in matched_skills]}")
        skill_instructions = "\n\n".join([
            f"--- Active Domain Skill: {s.name} ---\n{s.instructions}"
            for s in matched_skills
        ])
    else:
        print("[+] No specific domain skills matched for this request.")
        skill_instructions = "No specific domain skills active."
        
    for attempt in range(1, max_retries + 1):
        try:
            # Configure the session service
            session_service = InMemorySessionService()
            session = await session_service.create_session(
                app_name="agents",
                user_id=user_id,
                session_id=session_id,
                state={"skill_instructions": skill_instructions}
            )
            
            # Initialize App with GuardrailsPlugin
            app = App(
                name="agents",
                root_agent=root_agent,
                plugins=[GuardrailsPlugin()]
            )
            
            # Initialize the Runner with the configured App
            runner = Runner(app=app, session_service=session_service)
            
            # Execute the agents sequentially and stream/capture the events
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=new_message
            ):
                author = event.author
                if event.content and event.content.parts:
                    text = event.content.parts[0].text
                    if text:
                        print(f"--- Agent: {author} ---")
                        print(f"{text.strip()}\n")
            
            # Get the final state to show the results stored in the session
            session = await session_service.get_session(app_name="agents", user_id=user_id, session_id=session_id)
            print("--- Session State Capture ---")
            for key, val in session.state.items():
                print(f"Key '{key}':\n{str(val)[:300]}...\n")
            
            # Success!
            print("[+] Success: All agents executed sequentially and completed the task successfully.")
            return
            
        except Exception as e:
            # Check for direct or wrapped SecurityViolation from prompt injection
            if isinstance(e, SecurityViolation) or (isinstance(e, RuntimeError) and "Prompt injection" in str(e)):
                print("\n[-] Blocked by Guardrails: Access Denied: Prompt injection attempt detected.")
                sys.exit(0)
                
            error_str = str(e)
            if any(term in error_str for term in ["503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "LimitExceeded", "quota"]):
                wait_time = 20 if any(t in error_str for t in ["429", "RESOURCE_EXHAUSTED", "quota"]) else delay_seconds
                first_line = error_str.splitlines()[0] if error_str.splitlines() else "Unknown Error"
                clean_err = first_line if "429" not in first_line else "429 Resource Exhausted/Rate Limit"
                print(f"[!] Transient issue encountered on attempt {attempt}/{max_retries}: {clean_err}")
                print(f"Waiting {wait_time} seconds before retrying...")
                if attempt < max_retries:
                    await asyncio.sleep(wait_time)
                else:
                    print("[-] Max retries exceeded.")
                    raise e
            else:
                raise e

def main():
    # Allow passing custom test query via command line if needed
    query = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(run_pipeline_with_retry(query=query))

if __name__ == "__main__":
    main()
