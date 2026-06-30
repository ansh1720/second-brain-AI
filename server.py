"""
SecondBrain AI — Local Web Server
Serves the frontend and bridges HTTP requests to the ADK agent pipeline.

Run:  uv run python server.py
Then open: http://localhost:8765
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Reconfigure stdout for UTF-8 (Windows)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

from memory import init_db
from mcp_server.memory_tool import retrieve_memory as _retrieve
from skills import match_and_load_skills
from agents.guardrails import GuardrailsPlugin, SecurityViolation
from agents.agent import root_agent

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.apps import App
from google.genai import types

FRONTEND_DIR = Path(__file__).parent / "frontend"

init_db()


SESSION_SERVICE = InMemorySessionService()


def run_agent(query: str, session_id: str, history_data: list = None) -> dict:
    """Run the full multi-agent pipeline and return results."""

    async def _run():
        matched_skills = match_and_load_skills(query)
        skill_instructions = (
            "\n\n".join(f"--- Active Domain Skill: {s.name} ---\n{s.instructions}" for s in matched_skills)
            if matched_skills else "No specific domain skills active."
        )

        app = App(name="app", root_agent=root_agent, plugins=[GuardrailsPlugin()])
        runner = Runner(app=app, session_service=SESSION_SERVICE)

        # Retrieve or create session
        try:
            session = await SESSION_SERVICE.get_session(
                app_name="app",
                user_id="user_123",
                session_id=session_id
            )
            session.state["skill_instructions"] = skill_instructions
        except Exception:
            session = await SESSION_SERVICE.create_session(
                app_name="app",
                user_id="user_123",
                session_id=session_id,
                state={"skill_instructions": skill_instructions}
            )

        # Sync conversation history from client if new session or session restarted
        if history_data and not session.messages:
            session.messages = []
            for msg in history_data:
                role = msg.get("role")
                content = msg.get("content")
                if role and content:
                    adk_role = "user" if role == "user" else "model"
                    session.messages.append(
                        types.Content(role=adk_role, parts=[types.Part.from_text(text=content)])
                    )

        events = []
        async for event in runner.run_async(
            user_id="user_123",
            session_id=session_id,
            new_message=types.Content(role="user", parts=[types.Part.from_text(text=query)])
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        events.append({"author": event.author, "text": part.text})

        # Get updated session
        session = await SESSION_SERVICE.get_session(
            app_name="app", user_id="user_123", session_id=session_id
        )

        final = session.state.get("final_answer") or (events[-1]["text"] if events else "No response generated.")
        return {"final_answer": final, "events": events, "state": dict(session.state)}

    return asyncio.run(_run())


def get_memory() -> dict:
    """Retrieve key memory values for the UI."""
    keys = ["career_goals", "budget", "preferences", "decisions", "notes"]
    result = {}
    for k in keys:
        try:
            val = _retrieve(k)
            result[k] = val if val and "not found" not in val.lower() else None
        except Exception:
            result[k] = None
    return result


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[server] {args[0]} {args[1]} {args[2]}")

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path: Path, content_type: str):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/" or path == "/index.html":
            self.send_file(FRONTEND_DIR / "index.html", "text/html; charset=utf-8")
        elif path == "/memory":
            self.send_json(get_memory())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/ask":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            query = body.get("query", "").strip()
            session_id = body.get("session_id", "web_session")
            history_data = body.get("history", [])

            if not query:
                self.send_json({"error": "Query is empty"}, 400)
                return

            api_key = os.getenv("GEMINI_API_KEY", "")
            if not api_key or api_key == "YOUR_API_KEY":
                self.send_json({"error": "GEMINI_API_KEY not set in .env file"}, 500)
                return

            print(f"\n[+] Query: {query} (Session: {session_id})")
            try:
                result = run_agent(query, session_id, history_data)
                self.send_json(result)
            except SecurityViolation as e:
                self.send_json({"error": f"Blocked by guardrails: {e}"}, 403)
            except Exception as e:
                print(f"[!] Error: {e}")
                self.send_json({"error": str(e)}, 500)
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/memory":
            from urllib.parse import parse_qs
            query = parse_qs(parsed.query)
            key = query.get("key", [None])[0]

            from memory.clear_memory import clear_all_memory, delete_memory_key
            if key:
                success = delete_memory_key(key)
                action = f"delete key '{key}'"
            else:
                success = clear_all_memory()
                action = "clear all memory"

            if success:
                self.send_json({"success": True, "message": f"Successfully performed: {action}"})
            else:
                self.send_json({"error": f"Failed to perform: {action}"}, 500)
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or api_key == "YOUR_API_KEY":
        print("[-] Error: Set GEMINI_API_KEY in your .env file first.")
        sys.exit(1)

    port = 8765
    print(f"[+] SecondBrain AI server starting...")
    print(f"[+] Open your browser: http://localhost:{port}")
    print(f"[+] Press Ctrl+C to stop\n")
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()
