import os
import sys
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.genai.errors import APIError, ServerError

# Reconfigure stdout to use UTF-8 to prevent encoding errors with special symbols (e.g. Rupee sign)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import the root orchestrator agent
from agents.agent import root_agent

async def run_pipeline_with_retry(max_retries=5, delay_seconds=4):
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY":
        print("[-] Error: GEMINI_API_KEY is not configured in the .env file.")
        print("Please add your Gemini API Key to the .env file before running.")
        sys.exit(1)
        
    print("[+] Initializing Multi-Agent System (Sequential Orchestrator)...")
    
    user_id = "user_123"
    session_id = "session_456"
    
    query = "Should I buy a MacBook Air or Lenovo LOQ for AI development?"
    print(f"\n[+] User Request: {query}")
    print("[+] Executing workflow: Planner -> Memory -> Research -> Decision -> Reflection\n")
    
    new_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=query)]
    )
    
    for attempt in range(1, max_retries + 1):
        try:
            # Configure the session service (we recreate it to have a fresh state per clean run)
            session_service = InMemorySessionService()
            await session_service.create_session(app_name="agents", user_id=user_id, session_id=session_id)
            
            # Initialize the Runner with our orchestrator agent
            runner = Runner(agent=root_agent, app_name="agents", session_service=session_service)
            
            # Execute the agents sequentially and stream/capture the events
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=new_message
            ):
                author = event.author
                # Print transitions and updates from each agent
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
            
        except (ServerError, APIError) as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"[!] Transient model overload (503) on attempt {attempt}/{max_retries}. Retrying in {delay_seconds} seconds...")
                if attempt < max_retries:
                    await asyncio.sleep(delay_seconds)
                else:
                    print("[-] Max retries exceeded due to model unavailability.")
                    raise e
            else:
                raise e

def main():
    asyncio.run(run_pipeline_with_retry())

if __name__ == "__main__":
    main()
