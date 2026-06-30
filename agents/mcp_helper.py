import os
import sys

# Add project root to sys.path to ensure local imports resolve
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from mcp_server.search_tool import search_web
from mcp_server.memory_tool import save_memory, retrieve_memory
from mcp_server.calculator import calculator
from mcp_server.compare_tool import compare_options
from mcp_server.pdf_reader import read_pdf

def get_mcp_tools():
    """Returns the list of custom tool functions directly as callable Python tools.
    This bypasses MCP subprocess container limitations during CLI evaluation runs.
    """
    return [
        search_web,
        save_memory,
        retrieve_memory,
        calculator,
        compare_options,
        read_pdf
    ]

def get_mcp_toolset() -> McpToolset:
    """Returns an McpToolset wrapper connecting to the stdio MCP server subprocess.
    """
    python_exe = os.path.abspath(os.path.join(".venv", "Scripts", "python.exe"))
    if not os.path.exists(python_exe):
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
