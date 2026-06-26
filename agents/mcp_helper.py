import os
import sys
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

def get_mcp_toolset() -> McpToolset:
    # Get absolute path to python in the project's virtual environment
    python_exe = os.path.abspath(os.path.join(".venv", "Scripts", "python.exe"))
    if not os.path.exists(python_exe):
        # Fall back to sys.executable if running globally or outside virtualenv
        python_exe = sys.executable
        
    server_script = os.path.abspath(os.path.join("mcp_server", "server.py"))
    
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command=python_exe,
                args=[server_script],
            )
        )
    )
