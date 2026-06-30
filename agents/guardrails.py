import re
from typing import Any, Optional
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.base_agent import BaseAgent
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types

class SecurityViolation(ValueError):
    pass

class GuardrailsPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="secondbrain_guardrails")
        
        self.injection_patterns = [
            re.compile(r"ignore\s+(?:the\s+)?(?:previous\s+)?instructions", re.IGNORECASE),
            re.compile(r"ignore\s+(?:the\s+)?system\s+(?:prompt|instructions)", re.IGNORECASE),
            re.compile(r"reveal\s+(?:your\s+)?(?:instructions|system|prompt|memory)", re.IGNORECASE),
            re.compile(r"disregard\s+(?:all\s+)?prior\s+instructions", re.IGNORECASE),
            re.compile(r"bypass\s+restrictions", re.IGNORECASE),
            re.compile(r"jailbreak", re.IGNORECASE)
        ]
        
        self.allowlisted_tools = {
            "search_web",
            "save_memory",
            "retrieve_memory",
            "calculator",
            "compare_options",
            "read_pdf"
        }

    async def on_user_message_callback(
        self,
        *,
        invocation_context: Any,
        user_message: types.Content,
    ) -> Optional[types.Content]:
        text_content = ""
        if user_message.parts:
            for part in user_message.parts:
                if part.text:
                    text_content += part.text
                    
        # Check against injection patterns
        for pattern in self.injection_patterns:
            if pattern.search(text_content):
                print(f"[!] Guardrails Triggered: Prompt injection attempt detected in message: '{text_content}'")
                raise SecurityViolation("Access Denied: Prompt injection attempt detected.")
                
        # Dynamically load matching skills based on keywords
        from skills import match_and_load_skills
        matched_skills = match_and_load_skills(text_content)
        if matched_skills:
            print(f"[Guardrails] Injecting skills: {[s.name for s in matched_skills]}")
            skill_instructions = "\n\n".join([
                f"--- Active Domain Skill: {s.name} ---\n{s.instructions}"
                for s in matched_skills
            ])
        else:
            skill_instructions = "No specific domain skills active."
            
        # Store instructions in session state for prompt template formatting
        if hasattr(invocation_context, "session") and invocation_context.session:
            invocation_context.session.state["skill_instructions"] = skill_instructions
            
        return None

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
    ) -> Optional[dict]:
        # 1. Tool Allowlisting
        if tool.name not in self.allowlisted_tools:
            print(f"[!] Guardrails Triggered: Attempted to call unauthorized tool '{tool.name}'")
            return {"error": f"Tool '{tool.name}' is blocked by Guardrails policy."}
            
        # 2. Memory Access Restrictions
        if tool.name in ["save_memory", "retrieve_memory"]:
            key = tool_args.get("key", "")
            # Ensure key contains only safe alphanumeric/space/colons
            if not re.match(r"^[a-zA-Z0-9_\-\: ]+$", key):
                print(f"[!] Guardrails Triggered: Invalid memory key '{key}'")
                return {"error": "Access Denied: Memory keys must be alphanumeric and contain no special SQL or scripting characters."}
                
            # Restrict access to system files, env, credentials
            forbidden_keys = {"config", "password", "token", "env", "credential", "admin"}
            if any(f in key.lower() for f in forbidden_keys):
                print(f"[!] Guardrails Triggered: Attempted to access forbidden memory key '{key}'")
                return {"error": f"Access Denied: Access to system parameter '{key}' is restricted."}
                
        return None

    async def after_agent_callback(
        self,
        *,
        agent: BaseAgent,
        callback_context: CallbackContext,
    ) -> Optional[types.Content]:
        # Output validation for the final output
        if agent.name == "reflection_agent":
            output = callback_context.output
            if not output:
                return None
                
            text_content = ""
            if output.parts:
                for part in output.parts:
                    if part.text:
                        text_content += part.text
            
            # Sanitize insecure links if present in final text
            unsafe_patterns = [
                r"http://",
                r"ftp://",
                r"torrent",
                r"crack\s+software",
                r"bypass\s+paywall"
            ]
            
            for pat in unsafe_patterns:
                if re.search(pat, text_content, re.IGNORECASE):
                    print(f"[!] Guardrails Triggered: Unsafe link or claim detected in Reflection Agent output.")
                    sanitized_text = re.sub(r"http://", "https://", text_content, flags=re.IGNORECASE)
                    from google.genai.types import Content, Part
                    return Content(parts=[Part.from_text(text=sanitized_text)])
                    
        return None
